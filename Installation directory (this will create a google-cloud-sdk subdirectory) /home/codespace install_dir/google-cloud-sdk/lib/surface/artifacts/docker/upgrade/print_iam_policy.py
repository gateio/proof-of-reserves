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
"""Print an Artifact Registry IAM policy for Container Registry to Artifact Registry upgrade."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import flags
from googlecloudsdk.command_lib.artifacts import upgrade_util
from googlecloudsdk.command_lib.artifacts import util


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class PrintIamPolicy(base.Command):
  """Print an Artifact Registry IAM policy for Container Registry to Artifact Registry upgrade.

  Print an Artifact Registry IAM policy that is equivalent to the IAM policy
  applied to the storage bucket for the specified Container Registry hostname.
  Apply the returned policy to the Artifact Registry repository that will
  replace the specified host. If the project has an organization, this command
  analyzes IAM policies at the organization level. Otherwise, this command
  analyzes IAM policies at the project level. See required permissions at
  https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies#required-permissions.
  """

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES': """\
  To print an equivalent Artifact Registry IAM policy for 'gcr.io/my-project':

      $ {command} upgrade print-iam-policy gcr.io --project=my-project
  """,
  }

  @staticmethod
  def Args(parser):
    flags.GetGCRDomainArg().AddToParser(parser)

  def Run(self, args):
    """Runs the command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      An iam.Policy.
    """
    domain = args.DOMAIN
    project = util.GetProject(args)
    return upgrade_util.iam_policy(domain, project)
