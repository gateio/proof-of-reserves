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
"""Command to tail logs for a job."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.logs import read as read_logs_lib
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import streaming
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA)
class Tail(base.BinaryBackedCommand):
  """Tail logs for Cloud Run jobs."""

  detailed_help = {
      'DESCRIPTION':
          """\
          {command} tails log-entries for a particular
          Cloud Run job in real time.  The log entries are formatted for
          consumption in a terminal.
          """,
      'EXAMPLES':
          """\
          To tail log entries for a Cloud Run job, run:

            $ {command} my-job

          To tail log entries with severity ERROR or higher, run:

            $ {command} my-job --log-filter="severity>=ERROR"

          Detailed information about filters can be found at:
          [](https://cloud.google.com/logging/docs/view/advanced_filters)
          """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument('job', help='Name for a Cloud Run job.')
    read_logs_lib.LogFilterArgs(parser)

  def Run(self, args):
    filters = []
    if args.IsSpecified('log_filter'):
      filters.append(args.log_filter)
    filters.append('resource.type=%s' % 'cloud_run_job')
    filters.append('resource.labels.job_name=%s' % args.job)
    filters.append('resource.labels.location=%s' %
                   flags.GetRegion(args, prompt=True))
    filters.append('severity>=DEFAULT')
    project_id = properties.VALUES.core.project.Get(required=True)
    filter_str = ' '.join(filters)
    command_executor = streaming.LogStreamingWrapper()
    response = command_executor(
        project_id=project_id, log_format='run', log_filter=filter_str)
    return self._DefaultOperationResponseHandler(response)
