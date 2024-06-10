# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Implements the command to upload Generic artifacts to a repository."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os

from apitools.base.py import transfer
from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import flags
from googlecloudsdk.command_lib.artifacts import util
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources
from googlecloudsdk.core.util import scaled_integer


@base.ReleaseTracks(
    base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA, base.ReleaseTrack.GA
)
@base.Hidden
class Upload(base.Command):
  """Uploads an artifact to a generic repository."""

  api_version = 'v1'

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES': """\
    To upload version v0.1.0 of a generic artifact located in /path/to/file/ to a repository in "us-central1":

        $ {command} --location=us-central1 --project=myproject --repository=myrepo \
          --package=mypackage --version=v0.1.0 --source=/path/to/file/

    To upload version v0.1.0 of a generic artifact located in /path/to/file/ to a repository in "us-central1" within a folder structure:

        $ {command} --location=us-central1 --project=myproject --repository=myrepo \
          --package=mypackage --version=v0.1.0 --source=/path/to/file/ --destination-path=folder/file
    """,
  }

  @staticmethod
  def Args(parser):
    """Set up arguments for this command.

    Args:
      parser: An argparse.ArgumentPaser.
    """
    flags.GetRequiredRepoFlag().AddToParser(parser)
    flags.GetSkipExistingFlag().AddToParser(parser)
    base.ASYNC_FLAG.AddToParser(parser)
    group = parser.add_group(mutex=True, required=True)

    parser.add_argument(
        '--package',
        metavar='PACKAGE',
        required=True,
        help='The package to upload.')
    parser.add_argument(
        '--version',
        metavar='VERSION',
        required=True,
        help=(
            'The version of the package. '
            'You cannot overwrite an existing version in the repository.'
        ),
    )
    parser.add_argument(
        '--destination-path',
        metavar='DESTINATION_PATH',
        required=False,
        help=(
            'Use to specify the path to upload a generic '
            'artifact to within a folder structure.'
        ),
    )
    group.add_argument(
        '--source',
        metavar='SOURCE',
        help='The path to the file you are uploading.')
    group.add_argument(
        '--source-directory',
        metavar='SOURCE_DIRECTORY',
        help='The directory you are uploading.')

  def Run(self, args):
    """Run the generic artifact upload command."""

    client = apis.GetClientInstance('artifactregistry', self.api_version)
    messages = client.MESSAGES_MODULE

    source_dir = args.source_directory
    source_file = args.source

    if source_dir and args.async_:
      raise ar_exceptions.InvalidInputValueError(
          'Asynchronous uploads not supported for directories.'
      )

    if source_file and args.skip_existing:
      raise ar_exceptions.InvalidInputValueError(
          'Skip existing is not supported for single file uploads.'
      )
    # Uploading a single file
    if source_file:
      return self.uploadArtifact(args, source_file, client, messages)
    # Uploading a directory
    elif source_dir:
      # If source_dir was specified, expand, normalize and traverse
      # through the directory sending one upload request per file found,
      # preserving the folder structure.
      args.source_directory = os.path.normpath(os.path.expanduser(source_dir))
      if not os.path.isdir(args.source_directory):
        raise ar_exceptions.InvalidInputValueError(
            'Specified path is not an existing directory.'
            )
      log.status.Print('Uploading directory: {}'.format(source_dir))
      for path, _, files in os.walk(args.source_directory):
        for file in files:
          try:
            self.uploadArtifact(
                args, (os.path.join(path, file)), client, messages
            )
          except waiter.OperationError as e:
            if args.skip_existing and 'already exists' in str(e):
              log.warning(
                  'File with the same package and version already exists.'
              )
              continue
            raise

  def uploadArtifact(self, args, file_path, client, messages):
    # Default chunk size to be consistent for uploading to clouds.
    chunksize = scaled_integer.ParseInteger(
        properties.VALUES.storage.upload_chunk_size.Get()
    )
    repo_ref = args.CONCEPTS.repository.Parse()
    # If destination_path was not specified,
    # take the last portion of the file path as the the file name.
    # ie. file path is folder1/folder2/file.txt, the file name is file.txt
    if args.source:
      file_name = os.path.basename(file_path)
      if args.destination_path:
        path = os.path.normpath(args.destination_path)
        file_name = os.path.join(path, os.path.basename(file_path))
    else:
      # ie: "/usr/Desktop/test_generic_folder"
      # remove the prefix from the full file path
      # /usr/Desktop/test_generic_folder/test.txt
      # to get 'test.txt'
      file_name = file_path[len(args.source_directory)+1:]
      if args.destination_path:
        path = os.path.normpath(args.destination_path)
        file_name = os.path.join(path, file_name)

    # Windows uses "\" as its path separator, replace it with "/" to standardize
    # all file resource names.
    file_name = file_name.replace(os.sep, '/')
    request = messages.ArtifactregistryProjectsLocationsRepositoriesGenericArtifactsUploadRequest(
        uploadGenericArtifactRequest=messages.UploadGenericArtifactRequest(
            packageId=args.package,
            versionId=args.version,
            filename=file_name),
        parent=repo_ref.RelativeName())

    mime_type = util.GetMimetype(file_path)
    upload = transfer.Upload.FromFile(
        file_path, mime_type=mime_type, chunksize=chunksize)
    op_obj = client.projects_locations_repositories_genericArtifacts.Upload(
        request, upload=upload)
    op = op_obj.operation
    op_ref = resources.REGISTRY.ParseRelativeName(
        op.name, collection='artifactregistry.projects.locations.operations')

    # Handle the operation.
    if args.async_:
      return op_ref
    else:
      result = waiter.WaitFor(
          waiter.CloudOperationPollerNoResources(
              client.projects_locations_operations), op_ref,
          'Uploading file: {}'.format(file_name))
      return result
