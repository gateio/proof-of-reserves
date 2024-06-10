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
"""'workbench instances rollback' command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.workbench import instances as instance_util
from googlecloudsdk.api_lib.workbench import util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.workbench import flags

DETAILED_HELP = {
    'DESCRIPTION':
        """
        Rolls back a workbench instance.
    """,
    'EXAMPLES':
        """
    To rollback an instance, run:

        $ {command} example-instance target-snapshot=projects/example-project/global/snapshots/aorlbjvpavvf --location=us-central1-a
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Rollback(base.Command):
  """Rolls back a workbench instance."""

  @staticmethod
  def Args(parser):
    """Upgrade flags for this command."""
    flags.AddRollbackInstanceFlags(parser)

  def Run(self, args):
    release_track = self.ReleaseTrack()
    client = util.GetClient(release_track)
    messages = util.GetMessages(release_track)
    instance_service = client.projects_locations_instances
    operation = instance_service.Rollback(
        instance_util.CreateInstanceRollbackRequest(args, messages))
    return instance_util.HandleLRO(
        operation,
        args,
        instance_service,
        release_track,
        operation_type=instance_util.OperationType.ROLLBACK)


Rollback.detailed_help = DETAILED_HELP
