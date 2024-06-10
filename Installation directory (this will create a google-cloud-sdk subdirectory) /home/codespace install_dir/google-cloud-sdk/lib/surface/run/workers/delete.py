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
"""Command for deleting a worker."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import deletion
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import pretty_print
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Delete(base.Command):
  """Delete a worker."""

  detailed_help = {
      'DESCRIPTION':
          """\
          {description}
          """,
      'EXAMPLES':
          """\
          To delete a worker:

              $ {command} <worker-name>
          """,
  }

  @staticmethod
  def CommonArgs(parser):
    worker_presentation = presentation_specs.ResourcePresentationSpec(
        'WORKER',
        resource_args.GetWorkerResourceSpec(),
        'Worker to delete.',
        required=True,
        prefixes=False,
    )
    concept_parsers.ConceptParser([worker_presentation]).AddToParser(parser)
    flags.AddAsyncFlag(parser, default_async_for_cluster=True)

  @staticmethod
  def Args(parser):
    Delete.CommonArgs(parser)

  def _ConnectionContext(self, args):
    return connection_context.GetConnectionContext(
        args, flags.Product.RUN, self.ReleaseTrack()
    )

  def Run(self, args):
    """Delete a worker."""
    conn_context = self._ConnectionContext(args)
    worker_ref = args.CONCEPTS.worker.Parse()
    flags.ValidateResource(worker_ref)
    console_io.PromptContinue(
        message='Worker [{worker}] will be deleted.'.format(
            worker=worker_ref.servicesId),
        throw_if_unattended=True,
        cancel_on_no=True)

    async_ = deletion.AsyncOrDefault(args.async_)
    with serverless_operations.Connect(conn_context) as client:
      deletion.Delete(
          worker_ref, client.GetWorker, client.DeleteWorker, async_
      )
    if async_:
      pretty_print.Success(
          'Worker [{}] is being deleted.'.format(worker_ref.servicesId)
      )
    else:
      log.DeletedResource(worker_ref.servicesId, 'worker')
