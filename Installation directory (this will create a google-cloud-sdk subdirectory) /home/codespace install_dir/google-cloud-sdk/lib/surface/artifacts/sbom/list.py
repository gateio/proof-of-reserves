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
"""Implements the command to list SBOM file references."""


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import sbom_printer
from googlecloudsdk.command_lib.artifacts import sbom_util
from googlecloudsdk.core.resource import resource_printer


@base.ReleaseTracks(base.ReleaseTrack.GA)
class List(base.ListCommand):
  """List SBOM file references."""

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES': """\
          To list SBOM file references:

          $ {command}

          To list SBOM file references related to the image with the tag "us-east1-docker.pkg.dev/project/repo/my-image:1.0":

          $ {command} --resource="us-east1-docker.pkg.dev/project/repo/my-image:1.0"

          To list SBOM file references related to the image with the digest "us-east1-docker.pkg.dev/project/repo/my-image@sha256:88b205d7995332e10e836514fbfd59ecaf8976fc15060cd66e85cdcebe7fb356":

          $ {command} --resource="us-east1-docker.pkg.dev/project/repo/my-image@sha256:88b205d7995332e10e836514fbfd59ecaf8976fc15060cd66e85cdcebe7fb356"

          To list SBOM file references related to the images with the resource path prefix "us-east1-docker.pkg.dev/project/repo":

          $ {command} --resource-prefix="us-east1-docker.pkg.dev/project/repo"

          To list SBOM file references generated when the images were pushed to Artifact Registry and related to the installed package dependency "perl":

          $ {command} --dependency="perl"

          """,
  }

  @staticmethod
  def Args(parser):
    """Set up arguments for this command.

    Args:
      parser: An argparse.ArgumentPaser.
    """

    resource_printer.RegisterFormatter(
        sbom_printer.SBOM_PRINTER_FORMAT,
        sbom_printer.SbomPrinter,
        hidden=True)
    parser.display_info.AddFormat(sbom_printer.SBOM_PRINTER_FORMAT)

    base.SORT_BY_FLAG.SetDefault(parser, 'occ.create_time')
    base.URI_FLAG.RemoveFromParser(parser)
    group = parser.add_group(mutex=True)
    group.add_argument(
        '--dependency',
        required=False,
        help=(
            'List SBOM file references generated when the images were pushed to'
            ' Artifact Registry and related to the installed package'
            ' dependency. See'
            ' https://cloud.google.com/container-analysis/docs/scanning-types'
            ' for supported packages.'
        ),
    )
    group.add_argument(
        '--resource',
        required=False,
        help='List SBOM file references related to the image resource uri.',
    )
    group.add_argument(
        '--resource-prefix',
        required=False,
        help=(
            'List SBOM file references related to the resource uri with the'
            ' resource path prefix.'
        ),
    )

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      A list of SBOM references.
    """
    return sbom_util.ListSbomReferences(args)
