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
"""Perform maintenance command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.sole_tenancy.node_groups import flags
from googlecloudsdk.core import log
from googlecloudsdk.core.util import times


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class PerformMaintenance(base.UpdateCommand):
  """Perform maintenance on nodes in a Compute Engine node group."""

  detailed_help = {
      'brief': 'Perform maintenance on nodes in a Compute Engine node group.',
      'EXAMPLES': """
       To perform maintenance on nodes in a node group, run:

         $ {command} my-node-group --nodes=node-1,node-2 --start-time=2023-05-01T00:00:00.000-08:00
     """,
  }

  @staticmethod
  def Args(parser):
    flags.MakeNodeGroupArg().AddArgument(parser)
    flags.AddPerformMaintenanceNodesArgToParser(parser)
    flags.AddPerformMaintenanceStartTimeArgToParser(parser)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    messages = holder.client.messages

    node_group_ref = flags.MakeNodeGroupArg().ResolveAsResource(
        args,
        holder.resources,
        scope_lister=compute_flags.GetDefaultScopeLister(holder.client))

    perform_maintenance = messages.NodeGroupsPerformMaintenanceRequest(
        nodes=args.nodes
    )

    if args.start_time:
      perform_maintenance.startTime = times.FormatDateTime(args.start_time)

    request = messages.ComputeNodeGroupsPerformMaintenanceRequest(
        nodeGroupsPerformMaintenanceRequest=perform_maintenance,
        nodeGroup=node_group_ref.Name(),
        project=node_group_ref.project,
        zone=node_group_ref.zone)

    service = holder.client.apitools_client.nodeGroups
    operation = service.PerformMaintenance(request)
    operation_ref = holder.resources.Parse(
        operation.selfLink, collection='compute.zoneOperations')
    log.status.Print(
        'Perform maintenance call in progress for nodes [{}] in node group'
        ' [{}]: {}'.format(
            args.nodes, node_group_ref.Name(), operation_ref.SelfLink()
        )
    )
    log.status.Print(
        'Use [gcloud compute operations describe URI] to check the status of'
        ' the operation(s).'
    )
    return operation
