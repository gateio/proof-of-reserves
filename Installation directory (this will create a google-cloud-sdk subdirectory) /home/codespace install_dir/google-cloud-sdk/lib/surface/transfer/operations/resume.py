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
"""Command to resume a currently running transfer operation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.transfer import name_util


class Resume(base.Command):
  """Resume a currently paused transfer operation."""

  detailed_help = {
      'DESCRIPTION':
          """\
      Resume a currently paused transfer operation.
      """,
      'EXAMPLES':
          """\
      To resume an operation, run:

        $ {command} OPERATION-NAME
      """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'name',
        help='The name of the paused transfer operation you want to resume.')

  def Run(self, args):
    client = apis.GetClientInstance('transfer', 'v1')
    messages = apis.GetMessagesModule('transfer', 'v1')

    formatted_name = name_util.add_operation_prefix(args.name)
    client.transferOperations.Resume(
        messages.StoragetransferTransferOperationsResumeRequest(
            name=formatted_name))
