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
"""'workbench instances get-config' command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.workbench import instances as instance_util
from googlecloudsdk.api_lib.workbench import util
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import parser_errors
from googlecloudsdk.command_lib.workbench import flags
from googlecloudsdk.core import properties

DETAILED_HELP = {
    'DESCRIPTION':
        """
        Describes the valid configurations for workbench instances.
    """,
    'EXAMPLES':
        """
    For valid configurations, run:

        $ {command} --location=us-west1-a
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Describe(base.DescribeCommand):
  """Describes the valid configurations for workbench instances."""

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    flags.AddListInstanceFlags(parser)

  def Run(self, args):
    release_track = self.ReleaseTrack()
    client = util.GetClient(release_track)
    messages = util.GetMessages(release_track)
    if (not args.IsSpecified('location')) and (
        not properties.VALUES.notebooks.location.IsExplicitlySet()):
      raise parser_errors.RequiredError(argument='--location')
    instance_service = client.projects_locations_instances
    result = instance_service.GetConfig(
        instance_util.CreateGetConfigRequest(args, messages))
    return result

Describe.detailed_help = DETAILED_HELP
