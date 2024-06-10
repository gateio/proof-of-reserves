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
"""Download Artifact Registry files."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import tempfile

from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import download_util
from googlecloudsdk.command_lib.artifacts import file_util
from googlecloudsdk.command_lib.artifacts import flags
from googlecloudsdk.core import log


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Download(base.Command):
  """Download an Artifact Registry file.

  Downloads an Artifact Registry file based on file name.

  """

  detailed_help = {
      'DESCRIPTION':
          '{description}',
      'EXAMPLES':
          """\
      To download a file named `myfile` in project `my-project` under repository `my-repo` in `us-central1` to the local path `~/`:

          $ {command} --location=us-central1 --project=my-project --repository=my-repo --destination=~/ myfile

      To download a file named `myfile` in project `my-project` under repository `my-repo` in `us-central1` to the local path `~/` with file overwriting enabled:

          $ {command} --location=us-central1 --project=my-project --repository=my-repo --destination=~/ myfile --allow-overwrite
    """,
  }

  @staticmethod
  def Args(parser):
    flags.GetRequiredFileFlag().AddToParser(parser)
    flags.GetAllowOverwriteFlag().AddToParser(parser)
    parser.add_argument(
        '--destination',
        metavar='DESTINATION',
        required=True,
        help="""\
            The path where you want to download the file.""",
    )
    parser.add_argument(
        '--local-filename',
        metavar='LOCAL_FILENAME',
        help=(
            'If specified, the name of the downloaded file on the local system'
            ' is set to the value you use for LOCAL_FILENAME. Otherwise the'
            ' name of the downloaded file is based on the file name in the'
            ' registry.'
        ),
    )

  def Run(self, args):
    """Run the file download command."""

    # Escape slashes in the filesId.
    file_escaped = file_util.EscapeFileName(args.CONCEPTS.file.Parse())
    filename = (
        args.local_filename
        if args.local_filename
        else self.os_friendly_filename(file_escaped.filesId)
    )
    tmp_path = os.path.join(tempfile.gettempdir(), filename)
    final_path = os.path.join(args.destination, filename)
    final_path = os.path.expanduser(final_path)
    dest_dir = os.path.dirname(final_path)
    if not os.path.exists(dest_dir):
      raise ar_exceptions.DirectoryNotExistError(
          'Destination directory does not exist: ' + dest_dir
      )
    if not os.path.isdir(dest_dir):
      raise ar_exceptions.PathNotDirectoryError(
          'Destination is not a directory: ' + dest_dir
      )
    download_util.Download(
        tmp_path, final_path, file_escaped.RelativeName(), args.allow_overwrite
    )
    log.status.Print('Successfully downloaded the file to ' + args.destination)

  def os_friendly_filename(self, file_id):
    filename = file_id.replace(':', '%3A')
    filename = filename.replace('\\', '%5C')
    filename = filename.replace('*', '%3F')
    filename = filename.replace('?', '%22')
    filename = filename.replace('<', '%3C')
    filename = filename.replace('>', '%2E')
    filename = filename.replace('|', '%7C')
    return filename
