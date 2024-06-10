# -*- coding: utf-8 -*- #
# Copyright 2014 Google LLC. All Rights Reserved.
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

"""'logging logs list' command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager

from googlecloudsdk.api_lib.logging import util
from googlecloudsdk.calliope import base
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources


class List(base.ListCommand):
  """List your project's logs.

  Only logs that contain log entries are listed.

  ## EXAMPLES

  To list all logs in current project:

    $ {command}

  To list all logs for a view:

    $ {command} --bucket=[BUCKET_ID] --location=[LOCATION] --view=[VIEW_ID]
  """

  @staticmethod
  def Args(parser):
    base.PAGE_SIZE_FLAG.RemoveFromParser(parser)
    base.URI_FLAG.RemoveFromParser(parser)
    parser.display_info.AddFormat('table(.:label=NAME)')
    view_group = parser.add_argument_group(
        help='These arguments are used in conjunction with the parent to '
        'construct a view resource.')
    view_group.add_argument(
        '--location',
        required=True,
        metavar='LOCATION',
        help='Location of the log bucket.')
    view_group.add_argument(
        '--bucket',
        required=True,
        help='Id of the log bucket.')
    view_group.add_argument(
        '--view',
        required=True,
        help='Id of the view.')

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      The list of logs.
    """
    project = properties.VALUES.core.project.Get(required=True)

    project_ref = resources.REGISTRY.Parse(
        project, collection='cloudresourcemanager.projects')
    parent = project_ref.RelativeName()

    if args.IsSpecified('view'):
      # We are replacing the parent with the resourceName path for a view
      # instead of populating the resourceNames field.
      # This is due to the parent being a legacy required field.
      parent = util.CreateResourceName(
          util.CreateResourceName(
              util.CreateResourceName(parent, 'locations', args.location),
              'buckets', args.bucket), 'views', args.view)

    request = util.GetMessages().LoggingProjectsLogsListRequest(parent=parent)

    result = list_pager.YieldFromList(
        util.GetClient().projects_logs,
        request,
        field='logNames',
        limit=args.limit,
        batch_size=None,
        batch_size_attribute='pageSize')

    return result
