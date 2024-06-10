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
"""Command for obtaining details about a given worker."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import exceptions
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.run.printers import export_printer
from googlecloudsdk.command_lib.run.printers import worker_printer
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core.resource import resource_printer


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Describe(base.Command):
  """Obtain details about a given worker."""

  detailed_help = {
      'DESCRIPTION': """\
          {description}
          """,
      'EXAMPLES': """\
          To obtain details about a given worker:

              $ {command} <worker-name>

          To get those details in the YAML format:

              $ {command} <worker-name> --format=yaml

          To get them in YAML format suited to export (omitting metadata
          specific to this deployment and status info):

              $ {command} <worker-name> --format=export
          """,
  }

  @staticmethod
  def CommonArgs(parser):
    worker_presentation = presentation_specs.ResourcePresentationSpec(
        'WORKER',
        resource_args.GetWorkerResourceSpec(),
        'Worker to describe.',
        required=True,
        prefixes=False,
    )
    concept_parsers.ConceptParser([worker_presentation]).AddToParser(parser)

    resource_printer.RegisterFormatter(
        worker_printer.WORKER_PRINTER_FORMAT,
        worker_printer.WorkerPrinter, hidden=True)
    parser.display_info.AddFormat(worker_printer.WORKER_PRINTER_FORMAT)
    resource_printer.RegisterFormatter(
        export_printer.EXPORT_PRINTER_FORMAT,
        export_printer.ExportPrinter, hidden=True)

  @staticmethod
  def Args(parser):
    Describe.CommonArgs(parser)

  def _ConnectionContext(self, args):
    return connection_context.GetConnectionContext(
        args, flags.Product.RUN, self.ReleaseTrack()
    )

  def Run(self, args):
    """Obtain details about a given worker."""
    conn_context = self._ConnectionContext(args)
    worker_ref = args.CONCEPTS.worker.Parse()
    flags.ValidateResource(worker_ref)
    with serverless_operations.Connect(conn_context) as client:
      worker = client.GetWorker(worker_ref)
    if not worker:
      raise exceptions.ArgumentError('Cannot find worker [{}]'.format(
          worker_ref.servicesId))
    return worker
