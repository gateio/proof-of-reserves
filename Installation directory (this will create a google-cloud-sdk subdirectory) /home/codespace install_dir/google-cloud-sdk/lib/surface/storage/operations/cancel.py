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
"""Command to cancel a storage operation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.storage import api_factory
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.storage import operations_util
from googlecloudsdk.command_lib.storage import storage_url
from googlecloudsdk.core import log


class Cancel(base.Command):
  """Cancel a storage operation."""

  detailed_help = {
      'DESCRIPTION': """\
      Cancel a storage operation. Since operations are asynchronous, this
      request is best effort and may fail in cases such as when the operation
      is already complete.
      """,
      'EXAMPLES': """\
      To cancel the operation "C894F35J" on bucket "my-bucket", run:

        $ {command} projects/_/buckets/my-bucket/operations/C894F35J
      """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'operation_name',
        help=(
            'The operation name including the Cloud Storage bucket and'
            ' operation ID.'
        ),
    )

  def Run(self, args):
    bucket, operation_id = (
        operations_util.get_operation_bucket_and_id_from_name(
            args.operation_name
        )
    )
    scheme = storage_url.ProviderPrefix.GCS
    api_factory.get_api(scheme).cancel_operation(
        bucket_name=bucket, operation_id=operation_id
    )
    log.status.Print(
        'Sent cancel request for bucket {} operation {}'.format(
            storage_url.CloudUrl(scheme, bucket), operation_id
        )
    )
