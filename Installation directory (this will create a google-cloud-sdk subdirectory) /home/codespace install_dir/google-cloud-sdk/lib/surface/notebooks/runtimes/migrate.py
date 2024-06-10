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
"""'notebooks runtimes migrate' command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.notebooks import runtimes as runtime_util
from googlecloudsdk.api_lib.notebooks import util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.notebooks import flags

DETAILED_HELP = {
    'DESCRIPTION':
        """
        Request for migrating notebook runtimes.
    """,
    'EXAMPLES':
        """
    To migrate a runtime, run:

        $ {command} example-runtime --location=us-central1

    To migrate a runtime with a new custom network, run:

        $ {command} example-runtime --location=us-central1 --network=projects/example-project/global/networks/example-network --subnet=projects/example-project/regions/us-central1/subnetworks/example-subnetwork

    To migrate a runtime and reuse the post-startup script, run:

        $ {command} example-runtime --location=us-central1 --post-startup-script-option=POST_STARTUP_SCRIPT_OPTION_RERUN
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Migrate(base.Command):
  """Request for migrating runtimes."""

  @classmethod
  def Args(cls, parser):
    """Register flags for this command."""
    api_version = util.ApiVersionSelector(cls.ReleaseTrack())
    flags.AddMigrateRuntimeFlags(api_version, parser)

  def Run(self, args):
    """This is what gets called when the user runs this command."""
    release_track = self.ReleaseTrack()
    client = util.GetClient(release_track)
    messages = util.GetMessages(release_track)
    runtime_service = client.projects_locations_runtimes
    operation = runtime_service.Migrate(
        runtime_util.CreateRuntimeMigrateRequest(args, messages))
    return runtime_util.HandleLRO(
        operation,
        args,
        runtime_service,
        release_track,
        operation_type=runtime_util.OperationType.MIGRATE)


Migrate.detailed_help = DETAILED_HELP

