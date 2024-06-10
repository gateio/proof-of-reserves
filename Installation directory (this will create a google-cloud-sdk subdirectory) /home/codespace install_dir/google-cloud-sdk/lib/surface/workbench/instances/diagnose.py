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
"""'workbench instances diagnose' command."""

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
        Diagnoses a workbench instance.
    """,
    'EXAMPLES':
        """
    To diagnose an instance, run:

        $ {command} example-instance --location=us-west1-b --gcs-bucket=gs://example-bucket

    To diagnose an instance with a relative path:

        $ {command} example-instance --location=us-west1-b --gcs-bucket=gs://example-bucket --relative-path=logs

    To diagnose an instance, with packet capture:

        $ {command} example-instance --location=us-west1-b --gcs-bucket=gs://example-bucket --enable-packet-capture
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Diagnose(base.Command):
  """Diagnoses a workbench instance."""

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    flags.AddDiagnoseInstanceFlags(parser)

  def Run(self, args):
    """This is what gets called when the user runs this command."""
    release_track = self.ReleaseTrack()
    client = util.GetClient(release_track)
    messages = util.GetMessages(release_track)
    instance_service = client.projects_locations_instances
    operation = instance_service.Diagnose(
        instance_util.CreateInstanceDiagnoseRequest(args, messages))
    return instance_util.HandleLRO(
        operation,
        args,
        instance_service,
        release_track,
        operation_type=instance_util.OperationType.UPDATE)


Diagnose.detailed_help = DETAILED_HELP
