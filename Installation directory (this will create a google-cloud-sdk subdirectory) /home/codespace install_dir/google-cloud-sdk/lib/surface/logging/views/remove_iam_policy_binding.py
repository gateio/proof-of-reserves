# -*- coding: utf-8 -*- #
# Copyright 2024 Google Inc. All Rights Reserved.
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
"""'logging views remove_iam_policy_binding' command."""


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.logging import util
from googlecloudsdk.api_lib.util import exceptions as gcloud_exception
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.iam import iam_util


@base.ReleaseTracks(base.ReleaseTrack.GA)
@base.Hidden
class RemoveIamPolicyBinding(base.Command):
  """Remove IAM policy binding to a log view."""

  detailed_help = {
      'EXAMPLES': """\
          To remove an IAM policy binding for the role 'roles/my-role' for the user 'my-user@gmail.com' on my-view, run:

            $ {command} my-view --member='user:my-user@gmail.com' --role='roles/my-role' --bucket=my-bucket --location=global


          To remove a binding with a condition, run:

            $ {command} my-view --member='user:my-user@gmail.com' --role='roles/my-role' --bucket=my-bucket --location=global --condition=expression=[expression],title=[title],description=[description]

          See https://cloud.google.com/iam/docs/managing-policies for details about IAM policies and member types.
          """,
  }

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    parser.add_argument(
        'VIEW_ID', help='ID of the view that contains the IAM policy.'
    )
    util.AddParentArgs(parser, 'view that contains the IAM policy')
    util.AddBucketLocationArg(
        parser, True, 'Location of the bucket that contains the view.'
    )
    parser.add_argument(
        '--bucket',
        required=True,
        type=arg_parsers.RegexpValidator(r'.+', 'must be non-empty'),
        help='ID of the bucket that contains the view.',
    )
    iam_util.AddArgsForRemoveIamPolicyBinding(parser, add_condition=True)

  @gcloud_exception.CatchHTTPErrorRaiseHTTPException(
      'Status code: {status_code}. {status_message}.'
  )
  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      The updated policy.
    """
    view = util.CreateResourceName(
        util.CreateResourceName(
            util.GetBucketLocationFromArgs(args), 'buckets', args.bucket
        ),
        'views',
        args.VIEW_ID,
    )
    policy = util.GetIamPolicy(view)
    condition = iam_util.ValidateAndExtractCondition(args)
    iam_util.RemoveBindingFromIamPolicyWithCondition(
        policy=policy,
        member=args.member,
        role=args.role,
        condition=condition,
    )
    results = util.SetIamPolicy(view, policy)
    iam_util.LogSetIamPolicy(view, 'logging view')
    return results
