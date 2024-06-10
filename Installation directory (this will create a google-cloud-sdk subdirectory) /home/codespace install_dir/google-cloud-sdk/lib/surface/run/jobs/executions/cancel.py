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
"""Command for canceling executions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import cancellation
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import pretty_print
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core.console import console_io


class Cancel(base.Command):
  """Cancel an execution."""

  detailed_help = {
      'DESCRIPTION':
          """
          {description}
          """,
      'EXAMPLES':
          """
          To cancel an execution:

              $ {command} my-execution
          """,
  }

  @staticmethod
  def CommonArgs(parser):
    execution_presentation = presentation_specs.ResourcePresentationSpec(
        'EXECUTION',
        resource_args.GetExecutionResourceSpec(),
        'Execution to cancel.',
        required=True,
        prefixes=False)
    flags.AddAsyncFlag(parser, default_async_for_cluster=True, is_job=True)
    concept_parsers.ConceptParser([execution_presentation]).AddToParser(parser)

  @staticmethod
  def Args(parser):
    Cancel.CommonArgs(parser)

  def Run(self, args):
    """Cancel an execution."""
    conn_context = connection_context.GetConnectionContext(
        args, flags.Product.RUN, self.ReleaseTrack())
    ex_ref = args.CONCEPTS.execution.Parse()

    console_io.PromptContinue(
        message='Execution [{}] will be cancelled.'.format(ex_ref.executionsId),
        throw_if_unattended=True,
        cancel_on_no=True,
    )

    with serverless_operations.Connect(conn_context) as client:
      cancellation.Cancel(
          ex_ref, client.GetExecution, client.CancelExecution, args.async_
      )
    if args.async_:
      pretty_print.Success(
          'Execution [{}] is being cancelled.'.format(ex_ref.executionsId)
      )
    else:
      pretty_print.Success(
          'Cancelled execution [{}].'.format(ex_ref.executionsId)
      )
