# -*- coding: utf-8 -*- #
# Copyright 2020 Google LLC. All Rights Reserved.
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
"""'notebooks instances register' command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.notebooks import instances as instance_util
from googlecloudsdk.api_lib.notebooks import util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.notebooks import flags

DETAILED_HELP = {
    'DESCRIPTION':
        """
        Request for upgrading notebook instances.
    """,
    'EXAMPLES':
        """
    To upgrade an instance, run:

        $ {command} example-instance --location=us-central1-a
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA,
                    base.ReleaseTrack.GA)
class Upgrade(base.Command):
  """Request for upgrading instances."""

  @classmethod
  def Args(cls, parser):
    """Upgrade flags for this command."""
    api_version = util.ApiVersionSelector(cls.ReleaseTrack())
    flags.AddUpgradeInstanceFlags(api_version, parser)

  def Run(self, args):
    release_track = self.ReleaseTrack()
    client = util.GetClient(release_track)
    messages = util.GetMessages(release_track)
    instance_service = client.projects_locations_instances
    operation = instance_service.Upgrade(
        instance_util.CreateInstanceUpgradeRequest(args, messages))
    return instance_util.HandleLRO(
        operation,
        args,
        instance_service,
        release_track,
        operation_type=instance_util.OperationType.UPGRADE)


Upgrade.detailed_help = DETAILED_HELP
