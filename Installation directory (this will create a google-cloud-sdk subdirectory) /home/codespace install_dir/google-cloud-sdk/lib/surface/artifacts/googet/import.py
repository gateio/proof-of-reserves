# -*- coding: utf-8 -*- #
# Copyright 2021 Google LLC. All Rights Reserved.
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

"""Implements the command to import GooGet packages into a repository."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.command_lib.artifacts import flags
from googlecloudsdk.core import resources


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA,
                    base.ReleaseTrack.GA)
class Import(base.Command):
  """Import one or more GooGet packages into an artifact repository."""

  @staticmethod
  def Args(parser):
    """Set up arguements for this command.

    Args:
      parser: An argparse.ArgumentPaser.
    """
    flags.GetRepoArgFromBeta().AddToParser(parser)
    base.ASYNC_FLAG.AddToParser(parser)

    parser.add_argument(
        '--gcs-source',
        metavar='GCS_SOURCE',
        required=True,
        type=arg_parsers.ArgList(),
        help="""\
            The Google Cloud Storage location of a package to import.
            Wildcards may be added at the end to import multiple packages.""")

  def Run(self, args):
    """Run package import command."""
    client = apis.GetClientInstance('artifactregistry', 'v1')
    messages = client.MESSAGES_MODULE

    use_wildcard = False
    for gcs_source in args.gcs_source:
      if '*' in gcs_source:
        use_wildcard = True
        if not gcs_source.endswith('*'):
          raise exceptions.InvalidArgumentException(
              'GCS_SOURCE', 'Wildcards must be at the end of the GCS path.')

    repo_ref = args.CONCEPTS.repository.Parse()

    request = messages.ArtifactregistryProjectsLocationsRepositoriesGoogetArtifactsImportRequest(
        importGoogetArtifactsRequest=messages.ImportGoogetArtifactsRequest(
            gcsSource=messages.ImportGoogetArtifactsGcsSource(
                uris=args.gcs_source,
                useWildcards=use_wildcard,
            ),
        ),
        parent=repo_ref.RelativeName())

    op = client.projects_locations_repositories_googetArtifacts.Import(request)

    op_ref = resources.REGISTRY.ParseRelativeName(
        op.name, collection='artifactregistry.projects.locations.operations')

    if args.async_:
      return op_ref
    else:
      result = waiter.WaitFor(
          waiter.CloudOperationPollerNoResources(
              client.projects_locations_operations),
          op_ref, 'Importing package(s)')

      return result


Import.detailed_help = {
    'brief': 'Import one or more GooGet packages into an artifact repository.',
    'DESCRIPTION': """
      *{command}* imports GooGet packages from Google Cloud Storage into the specified
      artifact repository.
      """,
    'EXAMPLES': """
      To import the package `my-package.goo` from Google Cloud Storage into
      `my-repo`, run:

        $ {0} my-repo --location=us-central1 --gcs-source={1}

      To import the packages `my-package.goo` and `other-package.goo` into
      `my-repo`, run:

        $ {0} my-repo --location=us-central1 --gcs-source={1},{2}

      To import all packages from `my-directory` into `my-repo`, run:

        $ {0} my-repo --location=us-central1 --gcs-source={3}

      To import all packages in all subdirectories from a Google Cloud
      Storage bucket into `my-repo`, run:

        $ {0} my-repo --location=us-central1 --gcs-source={4}
    """.format('{command}', 'gs://my-bucket/path/to/my-package.goo',
               'gs://my-bucket/path/to/other-package.goo',
               'gs://my-bucket/my-directory/*',
               'gs://my-bucket/**')
}
