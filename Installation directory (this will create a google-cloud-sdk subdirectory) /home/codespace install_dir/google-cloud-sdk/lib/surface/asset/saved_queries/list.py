# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
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
"""Command to list Cloud Asset Inventory saved queries."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.asset import client_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.asset import flags
from googlecloudsdk.command_lib.asset import utils as asset_utils


class List(base.Command):
  """List Cloud Asset Inventory saved query."""

  detailed_help = {
      'DESCRIPTION':
          """\
      List Cloud Asset Inventory saved queries under a parent resource.
      """,
      'EXAMPLES':
          """\
        To list saved queries in organization 'org1', run:

          $ {command} --organization=org1
      """
  }

  @staticmethod
  def Args(parser):
    flags.AddParentArgs(parser, 'Project of the saved query.',
                        'Organization of the saved query.',
                        'Folder of the saved query.')

  def Run(self, args):
    parent = asset_utils.GetParentNameForExport(args.organization, args.project,
                                                args.folder)
    client = client_util.AssetSavedQueriesClient(parent)
    return client.List()
