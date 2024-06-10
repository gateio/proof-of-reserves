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
"""Implements the command to upload Go modules to a repository."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import tempfile

from apitools.base.py import transfer
from googlecloudsdk.api_lib.artifacts import exceptions
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import flags
from googlecloudsdk.command_lib.artifacts import go_util
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA,
                    base.ReleaseTrack.GA)
class Upload(base.Command):
  """Upload a Go module to an artifact repository."""

  api_version = 'v1'

  detailed_help = {
      'DESCRIPTION':
          '{description}',
      'EXAMPLES':
          """\
    To upload version v0.1.0 of a Go module located in /path/to/code/ to a repository in "us-central1":

        $ {command} --location=us-central1 --project=myproject --repository=myrepo \
          --module-path=the/module/path --version=v0.1.0 --source=/path/to/code
    """,
  }

  @staticmethod
  def Args(parser):
    """Set up arguements for this command.

    Args:
      parser: An argparse.ArgumentPaser.
    """
    flags.GetRequiredRepoFlag().AddToParser(parser)
    base.ASYNC_FLAG.AddToParser(parser)

    parser.add_argument(
        '--source',
        metavar='SOURCE',
        required=False,
        default='.',
        help='The root directory of the go module source code, '
        'defaults to the current directory.')
    parser.add_argument(
        '--module-path',
        metavar='MODULE_PATH',
        required=True,
        help='The module path of the Go module.')
    parser.add_argument(
        '--version',
        metavar='VERSION',
        required=True,
        help='The version of the Go module.')

  def Run(self, args):
    """Run the go module upload command."""

    client = apis.GetClientInstance('artifactregistry', self.api_version)
    client.additional_http_headers['X-Goog-Upload-Protocol'] = 'multipart'
    messages = client.MESSAGES_MODULE

    tempdir = tempfile.mkdtemp()
    # Create the go.zip file.
    zip_path = os.path.join(tempdir, 'go.zip')
    pack = go_util.PackOperation()
    pack_result = pack(
        module_path=args.module_path,
        version=args.version,
        source=args.source,
        output=zip_path)
    if pack_result.exit_code:
      raise exceptions.InvalidGoModuleError(
          'failed to package the go module: ' + pack_result.stderr)

    # Upload the go.zip.
    repo_ref = args.CONCEPTS.repository.Parse()
    request = messages.ArtifactregistryProjectsLocationsRepositoriesGoModulesUploadRequest(
        uploadGoModuleRequest=messages.UploadGoModuleRequest(),
        parent=repo_ref.RelativeName())
    upload = transfer.Upload.FromFile(zip_path, mime_type='application/zip')
    op_obj = client.projects_locations_repositories_goModules.Upload(
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
          'Uploading package')
      return result
