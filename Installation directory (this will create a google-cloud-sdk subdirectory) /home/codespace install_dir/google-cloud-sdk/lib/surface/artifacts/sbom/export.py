# -*- coding: utf-8 -*- #
# Copyright 2023 Google LLC. All Rights Reserved.
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
"""Implements the command to export SBOM files."""


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import sbom_util


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Export(base.Command):
  """Export SBOM files to Google Cloud Storage."""

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES': """\
          To export an SBOM file for the Artifact Registry image with URI "us-west1-docker.pkg.dev/my-project/my-repository/busy-box@sha256:abcxyz":

          $ {command} --uri=us-west1-docker.pkg.dev/my-project/my-repository/busy-box@sha256:abcxyz
          """,
  }

  @staticmethod
  def Args(parser):
    """Set up arguments for this command.

    Args:
      parser: An argparse.ArgumentPaser.
    """
    parser.display_info.AddFormat('yaml')
    parser.add_argument(
        '--uri',
        required=True,
        help=(
            'The URI of the Artifact Registry image the SBOM is exported for. A'
            " 'gcr.io' image can also be used if redirection is enabled in"
            ' Artifact Registry. Make sure'
            " 'artifactregistry.projectsettings.get' permission is granted to"
            ' the current gcloud user to verify the redirection status.'
        ),
    )

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: An argparse namespace. All the arguments that were provided to this
        command invocation.
    """
    sbom_util.ExportSbom(args)
