# -*- coding: utf-8 -*- #
# Copyright 2015 Google LLC. All Rights Reserved.
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
"""Displays log entries produced by Google Cloud Functions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime

from googlecloudsdk.api_lib.functions.v1 import util as util_v1
from googlecloudsdk.api_lib.functions.v2 import client as client_v2
from googlecloudsdk.api_lib.functions.v2 import exceptions
from googlecloudsdk.api_lib.logging import common as logging_common
from googlecloudsdk.api_lib.logging import util as logging_util
from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import parser_extensions
from googlecloudsdk.command_lib.functions import flags
from googlecloudsdk.command_lib.functions import util
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources
import six

_DEFAULT_TABLE_FORMAT = 'table(level,name,execution_id,time_utc,log)'
_DEFAULT_TABLE_FORMAT_V2 = 'table(level,name,time_utc,log)'

_EXECUTION_ID_NOT_SUPPORTED = (
    '`execution_id` is not supported in Cloud Functions v2.'
)


def _GetFunctionRef(name):
  # type: (str) -> resources.Resource | None
  if not name:
    return None

  return resources.REGISTRY.Parse(
      name,
      params={
          'projectsId': properties.VALUES.core.project.GetOrFail(),
          'locationsId': properties.VALUES.functions.region.GetOrFail(),
      },
      collection='cloudfunctions.projects.locations.functions',
  )


def _CreateGen1LogFilterBase(function_ref, region):
  """Generates Gen1-specific log filter base."""
  log_filter = [
      'resource.type="cloud_function"',
      'resource.labels.region="{}"'.format(region),
      'logName:"cloud-functions"',
  ]

  if function_ref:
    function_id = function_ref.functionsId
    log_filter.append('resource.labels.function_name="{}"'.format(function_id))

  return ' '.join(log_filter)


def _CreateGen2LogFilterBase(function_ref, region):
  """Generates Gen2-specific log filter base."""
  log_filter = [
      'resource.type="cloud_run_revision"',
      'resource.labels.location="{}"'.format(region),
      'logName:"run.googleapis.com"',
      'labels."goog-managed-by"="cloudfunctions"',
  ]

  if function_ref:
    # To conform to Cloud Run resource formats, GCFv2 functions' service names
    # are the function ID lower-cased with '_' replaced with '-'.
    # Context: go/upper-case-function-ids
    service_name = function_ref.functionsId.lower().replace('_', '-')
    log_filter.append('resource.labels.service_name="{}"'.format(service_name))

  return ' '.join(log_filter)


def _CreateLogFilter(args):
  # type: (parser_extensions.Namespace) -> str
  """Creates the filter for retrieving function logs based on the given args.


  Args:
    args: The arguments that were provided to this command invocation.

  Returns:
  """
  function_ref = _GetFunctionRef(args.name)
  region = properties.VALUES.functions.region.GetOrFail()

  if flags.ShouldUseGen1():
    log_filter = [_CreateGen1LogFilterBase(function_ref, region)]
  elif flags.ShouldUseGen2():
    log_filter = [_CreateGen2LogFilterBase(function_ref, region)]
  else:
    log_filter = [
        '({}) OR ({})'.format(
            _CreateGen1LogFilterBase(function_ref, region),
            _CreateGen2LogFilterBase(function_ref, region),
        )
    ]

  # Append common filters
  if args.execution_id:
    # This is currently only supported for gen1 but is applied "commonly" so
    # that Cloud Run logs filter out.
    log_filter.append('labels.execution_id="{}"'.format(args.execution_id))
  if args.min_log_level:
    log_filter.append('severity>={}'.format(args.min_log_level.upper()))
  if args.end_time:
    log_filter.append(
        'timestamp<="{}"'.format(logging_util.FormatTimestamp(args.end_time))
    )
  log_filter.append(
      'timestamp>="{}"'.format(
          logging_util.FormatTimestamp(
              args.start_time
              or datetime.datetime.utcnow() - datetime.timedelta(days=7)
          )
      )
  )

  return ' '.join(log_filter)


def _YieldLogEntries(entries):
  """Processes the given entries to yield rows.

  Args:
    entries: the log entries to process.

  Yields:
    Rows with level, name, execution_id, time_utc, and log properties.
  """
  for entry in entries:
    message = entry.textPayload
    if entry.jsonPayload:
      props = [
          prop.value
          for prop in entry.jsonPayload.additionalProperties
          if prop.key == 'message'
      ]
      if len(props) == 1 and hasattr(props[0], 'string_value'):
        message = props[0].string_value
    row = {'log': message}
    if entry.severity:
      severity = six.text_type(entry.severity)
      if severity in flags.SEVERITIES:
        # Use short form (first letter) for expected severities.
        row['level'] = severity[0]
      else:
        # Print full form of unexpected severities.
        row['level'] = severity
    if entry.resource and entry.resource.labels:
      for label in entry.resource.labels.additionalProperties:
        if label.key in ['function_name', 'service_name']:
          row['name'] = label.value
    if entry.labels:
      for label in entry.labels.additionalProperties:
        if label.key == 'execution_id':
          row['execution_id'] = label.value
    if entry.timestamp:
      row['time_utc'] = util.FormatTimestamp(entry.timestamp)
    yield row


@base.ReleaseTracks(base.ReleaseTrack.GA)
class GetLogs(base.ListCommand):
  """Display log entries produced by Google Cloud Functions."""

  @staticmethod
  def Args(parser):
    # type: (parser_extensions.ArgumentParser) -> None
    """Register flags for this command."""
    flags.AddRegionFlag(
        parser,
        help_text='Only show logs generated by functions in the region.',
    )
    base.LIMIT_FLAG.RemoveFromParser(parser)
    parser.add_argument(
        'name',
        nargs='?',
        help=(
            'Name of the function which logs are to be displayed. If no name '
            'is specified, logs from all functions are displayed.'
        ),
    )
    parser.add_argument(
        '--execution-id',
        help='Execution ID for which logs are to be displayed.',
    )
    parser.add_argument(
        '--start-time',
        required=False,
        type=arg_parsers.Datetime.Parse,
        help=(
            'Return only log entries in which timestamps are not earlier '
            'than the specified time. If *--start-time* is not specified, a '
            'default start time of 1 week ago is assumed. See $ gcloud '
            'topic datetimes for information on time formats.'
        ),
    )
    parser.add_argument(
        '--end-time',
        required=False,
        type=arg_parsers.Datetime.Parse,
        help=(
            'Return only log entries which timestamps are not later than '
            'the specified time. If *--end-time* is specified but '
            '*--start-time* is not, the command returns *--limit* latest '
            'log entries which appeared before --end-time. See '
            '*$ gcloud topic datetimes* for information on time formats.'
        ),
    )
    parser.add_argument(
        '--limit',
        required=False,
        type=arg_parsers.BoundedInt(1, 1000),
        default=20,
        help=(
            'Number of log entries to be fetched; must not be greater than '
            '1000. Note that the most recent entries in the specified time '
            'range are returned, rather than the earliest.'
        ),
    )
    flags.AddMinLogLevelFlag(parser)
    parser.display_info.AddCacheUpdater(None)

    flags.AddGen2Flag(parser)

  @util_v1.CatchHTTPErrorRaiseHTTPException
  def Run(self, args):
    # type: (parser_extensions.Namespace) -> None
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      A generator of objects representing log entries.
    """
    if not args.IsSpecified('format'):
      args.format = (
          _DEFAULT_TABLE_FORMAT_V2
          if flags.ShouldUseGen2()
          else _DEFAULT_TABLE_FORMAT
      )

    if flags.ShouldUseGen2() and args.execution_id:
      raise exceptions.FunctionsError(_EXECUTION_ID_NOT_SUPPORTED)

    log_filter = _CreateLogFilter(args)
    entries = list(
        logging_common.FetchLogs(log_filter, order_by='DESC', limit=args.limit)
    )

    if args.name and not entries:
      client = client_v2.FunctionsClient(self.ReleaseTrack())
      function_ref = _GetFunctionRef(args.name)
      if not client.GetFunction(function_ref.RelativeName()):
        # The function doesn't exist in the given region.
        log.warning(
            'There is no function named `{}` in region `{}`. Perhaps you '
            'meant to specify `--region` or update the `functions/region` '
            'configuration property?'.format(
                function_ref.functionsId, function_ref.locationsId
            )
        )

    return _YieldLogEntries(entries)


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class GetLogsBeta(GetLogs):
  """Display log entries produced by Google Cloud Functions."""


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class GetLogsAlpha(GetLogsBeta):
  """Display log entries produced by Google Cloud Functions."""
