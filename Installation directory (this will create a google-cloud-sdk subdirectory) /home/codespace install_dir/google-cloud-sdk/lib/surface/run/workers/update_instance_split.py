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
"""Command for updating instances split for worker resource."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from googlecloudsdk.api_lib.run import k8s_object
from googlecloudsdk.api_lib.run import traffic_pair
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import display
from googlecloudsdk.command_lib.run import config_changes
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import exceptions
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import pretty_print
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.run import stages
from googlecloudsdk.command_lib.run.printers import instance_split_printer
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core.console import progress_tracker
from googlecloudsdk.core.resource import resource_printer


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class AdjustInstanceSplit(base.Command):
  """Adjust the instance assignments for a Cloud Run worker."""

  detailed_help = {
      'DESCRIPTION': """\
          {description}
          """,
      'EXAMPLES': """\
          To assign 10% of instances to revision my-worker-s5sxn and
          90% of instances to revision my-worker-cp9kw run:

              $ {command} my-worker --to-revisions=my-worker-s5sxn=10,my-worker-cp9kw=90

          To increase the instances to revision my-worker-s5sxn to 20% and
          by reducing the instances to revision my-worker-cp9kw to 80% run:

              $ {command} my-worker --to-revisions=my-worker-s5sxn=20

          To rollback to revision my-worker-cp9kw run:

              $ {command} my-worker --to-revisions=my-worker-cp9kw=100

          To assign 100% of instances to the current or future LATEST revision
          run:

              $ {command} my-worker --to-latest

          You can also refer to the current or future LATEST revision in
          --to-revisions by the string "LATEST". For example, to set 10% of
          instances to always float to the latest revision:

              $ {command} my-worker --to-revisions=LATEST=10

         """,
  }

  @classmethod
  def CommonArgs(cls, parser):
    worker_presentation = presentation_specs.ResourcePresentationSpec(
        'WORKER',
        resource_args.GetWorkerResourceSpec(prompt=True),
        'Worker to update instance split of.',
        required=True,
        prefixes=False,
    )
    flags.AddAsyncFlag(parser)
    flags.AddUpdateInstanceSplitFlags(parser)
    flags.AddBinAuthzBreakglassFlag(parser)
    concept_parsers.ConceptParser([worker_presentation]).AddToParser(parser)

    resource_printer.RegisterFormatter(
        instance_split_printer.INSTANCE_SPLIT_PRINTER_FORMAT,
        instance_split_printer.InstanceSplitPrinter,
        hidden=True,
    )
    parser.display_info.AddFormat(
        instance_split_printer.INSTANCE_SPLIT_PRINTER_FORMAT
    )

  @classmethod
  def Args(cls, parser):
    cls.CommonArgs(parser)

  # TODO(b/322180968): Once Worker API is ready, replace anything in the
  # context of 'traffic' into 'instance split.'
  def Run(self, args):
    """Update the instance split for the worker.

    Args:
      args: Args!

    Returns:
      List of traffic.TrafficTargetStatus instances reflecting the change.
    """
    conn_context = connection_context.GetConnectionContext(
        args, flags.Product.RUN, self.ReleaseTrack()
    )
    worker_ref = args.CONCEPTS.worker.Parse()
    flags.ValidateResource(worker_ref)

    changes = flags.GetWorkerConfigurationChanges(args)
    if not changes:
      raise exceptions.NoConfigurationChangeError(
          'No instance split configuration change requested.'
      )
    changes.insert(
        0,
        config_changes.DeleteAnnotationChange(
            k8s_object.BINAUTHZ_BREAKGLASS_ANNOTATION
        ),
    )
    changes.append(
        config_changes.SetLaunchStageAnnotationChange(self.ReleaseTrack())
    )

    with serverless_operations.Connect(conn_context) as client:
      instance_split_stages = stages.UpdateInstanceSplitStages()
      try:
        with progress_tracker.StagedProgressTracker(
            'Updating instance split...',
            instance_split_stages,
            failure_message='Updating intance split failed',
            suppress_output=args.async_,
        ) as tracker:
          worker = client.UpdateInstanceSplit(
              worker_ref,
              changes,
              tracker,
              args.async_,
          )
      except Exception:
        worker = client.GetWorker(worker_ref)
        if worker:
          resources = traffic_pair.GetTrafficTargetPairs(
              worker.spec_traffic,
              worker.status_traffic,
              True,  # is_managed
              worker.status.latestReadyRevisionName,
              worker.status.url,
          )
          display.Displayer(
              self, args, resources, display_info=args.GetDisplayInfo()
          ).Display()
        raise

      if args.async_:
        pretty_print.Success('Updating instance split asynchronously.')
      else:
        resources = traffic_pair.GetTrafficTargetPairs(
            worker.spec_traffic,
            worker.status_traffic,
            True,  # is_managed
            worker.status.latestReadyRevisionName,
            worker.status.url,
        )
        return resources
