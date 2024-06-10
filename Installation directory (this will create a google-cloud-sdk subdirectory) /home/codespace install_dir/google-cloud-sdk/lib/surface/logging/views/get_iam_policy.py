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
"""'logging views get_iam_policy' command."""


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.logging import util
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base

DETAILED_HELP = {
    'DESCRIPTION': """
        Get the IAM policy for a view.
    """,
    'EXAMPLES': """
     To describe a view in a project, run:

        $ {command} my-view --bucket=my-bucket --location=global
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.GA)
@base.Hidden
class GetIamPolicy(base.Command):
  """Display the IAM policy for a view."""

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    parser.add_argument('VIEW_ID', help='ID of the view to fetch IAM policy')
    util.AddParentArgs(parser, 'view to fetch IAM policy')
    util.AddBucketLocationArg(
        parser, True, 'Location of the bucket that contains the view'
    )
    parser.add_argument(
        '--bucket',
        required=True,
        type=arg_parsers.RegexpValidator(r'.+', 'must be non-empty'),
        help='ID of the bucket that holds the view.',
    )

  def Run(self, args):
    """This is what get-iam-policy called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      The IAM policy for the specified view
    """
    view = util.CreateResourceName(
        util.CreateResourceName(
            util.GetBucketLocationFromArgs(args), 'buckets', args.bucket
        ),
        'views',
        args.VIEW_ID,
    )
    return util.GetIamPolicy(view)


GetIamPolicy.detailed_help = DETAILED_HELP
