# -*- coding: utf-8 -*- #
# Copyright 2024 Google LLC. All Rights Reserved.
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
"""Command for listing available workers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.run import global_methods
from googlecloudsdk.api_lib.run import service
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import commands
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import pretty_print
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class List(commands.List):
  """List available workers."""

  detailed_help = {
      'DESCRIPTION': """\
          {description}
          """,
      'EXAMPLES': """\
          To list available workers:

              $ {command}
          """,
  }

  @classmethod
  def CommonArgs(cls, parser):
    namespace_presentation = presentation_specs.ResourcePresentationSpec(
        '--namespace',
        resource_args.GetNamespaceResourceSpec(),
        'Namespace to list workers in.',
        required=True,
        prefixes=False,
    )
    concept_parsers.ConceptParser([namespace_presentation]).AddToParser(parser)

    parser.display_info.AddUriFunc(cls._GetResourceUri)

  @classmethod
  def Args(cls, parser):
    cls.CommonArgs(parser)

  def _SetFormat(self, args):
    """Set display format for output.

    Args:
      args: Namespace, the args namespace
    """
    columns = [
        pretty_print.READY_COLUMN,
        'firstof(id,metadata.name):label=WORKER',
    ]
    columns.append('region:label=REGION')
    columns.extend([
        'last_modifier:label="LAST DEPLOYED BY"',
        'last_transition_time:label="LAST DEPLOYED AT"',
    ])
    args.GetDisplayInfo().AddFormat(
        'table({columns}):({alias})'.format(
            columns=','.join(columns), alias=commands.SATISFIES_PZS_ALIAS
        )
    )

  def _GlobalList(self, client):
    """Provides the method to provide a regionless list."""
    return global_methods.ListWorkers(client)

  # For Workers private preview, workers are services underneath the table.
  # Adding a logic to only show services that are configured to behave
  # like workers. Checking for ingress==none
  def _FilterServices(self, workers):
    return list(filter(
        lambda w: w.annotations.get(service.INGRESS_ANNOTATION) == 'none',
        workers,
    ))

  def Run(self, args):
    """List available workers."""
    self._SetFormat(args)
    workers = []
    if not args.IsSpecified('region'):
      client = global_methods.GetServerlessClientInstance()
      self.SetPartialApiEndpoint(client.url)
      args.CONCEPTS.namespace.Parse()  # Error if no proj.
      # Don't consider region property here, we'll default to all regions
      workers = commands.SortByName(self._GlobalList(client))
    else:
      conn_context = connection_context.GetConnectionContext(
          args, flags.Product.RUN, self.ReleaseTrack()
      )
      namespace_ref = args.CONCEPTS.namespace.Parse()
      with serverless_operations.Connect(conn_context) as operations:
        self.SetCompleteApiEndpoint(conn_context.endpoint)
        workers = commands.SortByName(
            operations.ListWorkers(namespace_ref)
        )
    return self._FilterServices(workers)
