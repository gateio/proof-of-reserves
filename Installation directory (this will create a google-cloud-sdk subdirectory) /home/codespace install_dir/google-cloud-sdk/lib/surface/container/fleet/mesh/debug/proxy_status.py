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
"""Capture client sync status."""

from googlecloudsdk.api_lib.container.fleet import debug_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.container.fleet import resources
from googlecloudsdk.command_lib.container.fleet.mesh import istioctl_backend
from googlecloudsdk.core import properties

# Pull out the example text so the example command can be one line without the
# py linter complaining. The docgen tool properly breaks it into multiple lines.
EXAMPLES = r"""
    Retrieve the configuration sync status of all the proxies with the control
      plane.

      Example: ${command} --project=projectId --membership=membershipId --location=us-central1

    Print the config dump from both control plane and envoy for the given pod_name

      Example: ${command} pod_name --project=projectId --membership=membershipId --location=us-central1
"""


class ProxyStatus(base.BinaryBackedCommand):
  """Retrive the envoy configuration sync status or the detailed config dump.
  """
  detailed_help = {'EXAMPLES': EXAMPLES}

  @staticmethod
  def Args(parser):
    resources.AddMembershipResourceArg(
        parser,
        plural=False,
        membership_required=True,
        membership_help='Name of the membership to troubleshoot against.',
    )
    parser.add_argument(
        'pod_name',
        nargs='?',
        help=(
            'If applied, capture the detailed config dump from both control'
            ' plane and Envoy.'
        ),
    )

  def Run(self, args):
    command_executor = istioctl_backend.IstioctlWrapper()
    # Generate kubecontext
    context = debug_util.ContextGenerator(args)
    # Generate meshname for the target membership
    mesh_name, project_number = debug_util.MeshInfoGenerator(args)

    auth_cred = istioctl_backend.GetAuthToken(
        account=properties.VALUES.core.account.Get(), operation='apply'
    )
    # pod_name = args.pod_name if args.pod_name else ''
    response = command_executor(
        command='proxy-status',
        pod_name=args.pod_name,
        context=context,
        mesh_name=mesh_name,
        project_number=project_number,
        env=istioctl_backend.GetEnvArgsForCommand(
            extra_vars={'GCLOUD_AUTH_PLUGIN': 'true'}
        ),
        stdin=auth_cred,
    )
    return response
