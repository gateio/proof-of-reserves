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
"""Command to create a SHA custom module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.scc.manage.sha import clients
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.scc.manage import constants
from googlecloudsdk.command_lib.scc.manage import flags
from googlecloudsdk.command_lib.scc.manage import parsing


@base.ReleaseTracks(base.ReleaseTrack.GA, base.ReleaseTrack.ALPHA)
class Create(base.Command):
  """Create an Security Health Analytics custom module.

  ## EXAMPLES

  To create a Security Health Analytics custom module for organization
  `123`, run:

    $ {command} --organization=organizations/123
        --display-name="test_display_name"
        --enablement-state="ENABLED"
        --custom-config-from-file=custom_config.yaml
  """

  @staticmethod
  def Args(parser):
    flags.CreateParentFlag(required=True).AddToParser(parser)
    flags.CreateValidateOnlyFlag(required=False).AddToParser(parser)
    flags.CreateCustomConfigFlag(required=True).AddToParser(parser)
    flags.CreateEnablementStateFlag(
        module_type=constants.CustomModuleType.SHA,
        required=True
    ).AddToParser(parser)
    flags.CreateDisplayNameFlag(required=True).AddToParser(parser)

  def Run(self, args):
    parent = parsing.GetParentResourceNameFromArgs(args)
    validate_only = args.validate_only
    custom_config = parsing.GetCustomConfigFromArgs(
        args.custom_config_from_file,
    )
    enablement_state = parsing.GetEnablementStateFromArgs(
        args.enablement_state,
        module_type=constants.CustomModuleType.SHA
    )
    display_name = args.display_name

    client = clients.SHACustomModuleClient()

    return client.Create(
        parent=parent,
        validate_only=validate_only,
        custom_config=custom_config,
        enablement_state=enablement_state,
        display_name=display_name,
    )
