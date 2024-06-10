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
"""Capture cluster information and logs into archive to help diagnose problems."""

from googlecloudsdk.api_lib.container.fleet import debug_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.container.fleet import resources
from googlecloudsdk.command_lib.container.fleet.mesh import istioctl_backend
from googlecloudsdk.core import properties


class BugReport(base.BinaryBackedCommand):
  """Capture cluster information and logs into archive to help diagnose problems.

  Example: ${command} --project projectId
                      --membership membershipId
                      --location location
  """

  @staticmethod
  def Args(parser):
    resources.AddMembershipResourceArg(
        parser, plural=False,
        membership_required=True,
        membership_help='Name of the membership to troubleshoot against.'
    )

  def Run(self, args):
    command_executor = istioctl_backend.IstioctlWrapper()
    context = debug_util.ContextGenerator(args)
    auth_cred = istioctl_backend.GetAuthToken(
        account=properties.VALUES.core.account.Get(), operation='apply'
    )
    response = command_executor(
        command='bug-report',
        context=context,
        env=istioctl_backend.GetEnvArgsForCommand(
            extra_vars={'GCLOUD_AUTH_PLUGIN': 'true'}
        ),
        stdin=auth_cred,
    )
    return response
