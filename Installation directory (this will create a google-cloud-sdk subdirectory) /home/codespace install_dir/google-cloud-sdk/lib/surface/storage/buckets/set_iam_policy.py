# -*- coding: utf-8 -*- #
# Copyright 2021 Google LLC. All Rights Reserved.
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
"""Implementation of buckets set-iam-policy command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.storage import cloud_api
from googlecloudsdk.api_lib.storage.gcs_json import metadata_field_converters
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.iam import iam_util
from googlecloudsdk.command_lib.storage import errors_util
from googlecloudsdk.command_lib.storage import flags
from googlecloudsdk.command_lib.storage import iam_command_util
from googlecloudsdk.command_lib.storage import storage_url
from googlecloudsdk.command_lib.storage import wildcard_iterator
from googlecloudsdk.command_lib.storage.tasks import set_iam_policy_task


def _set_iam_policy_task_iterator(url_strings, policy):
  """Generates SetIamPolicyTask's for execution."""
  for url_string in url_strings:
    for resource in wildcard_iterator.get_wildcard_iterator(
        url_string, fields_scope=cloud_api.FieldsScope.SHORT):
      yield set_iam_policy_task.SetBucketIamPolicyTask(
          resource.storage_url, policy
      )


class SetIamPolicy(base.Command):
  """Set the IAM policy for a bucket."""

  detailed_help = {
      'DESCRIPTION':
          """
      Set the IAM policy for a bucket. For more information, see [Cloud
      Identity and Access
      Management](https://cloud.google.com/storage/docs/access-control/iam).
      """,
      'EXAMPLES':
          """
      To set the IAM policy in POLICY-FILE on BUCKET:

        $ {command} gs://BUCKET POLICY-FILE

      To set the IAM policy in POLICY-FILE on all buckets beginning with "b":

        $ {command} gs://b* POLICY-FILE
      """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'urls',
        nargs='+',
        help='URLs for buckets to apply the IAM policy to.'
        ' Can include wildcards.')
    parser.add_argument(
        '-e',
        '--etag',
        help='Custom etag to set on IAM policy. API will reject etags that do'
        ' not match this value, making it useful as a precondition during'
        ' concurrent operations.')
    iam_util.AddArgForPolicyFile(parser)
    flags.add_continue_on_error_flag(parser)

  def Run(self, args):
    for url_string in args.urls:
      url = storage_url.storage_url_from_string(url_string)
      errors_util.raise_error_if_not_gcs_bucket(args.command_path, url)

    policy = metadata_field_converters.process_iam_file(
        args.policy_file, custom_etag=args.etag)
    exit_code, output = iam_command_util.execute_set_iam_task_iterator(
        _set_iam_policy_task_iterator(args.urls, policy),
        args.continue_on_error)

    self.exit_code = exit_code
    return output
