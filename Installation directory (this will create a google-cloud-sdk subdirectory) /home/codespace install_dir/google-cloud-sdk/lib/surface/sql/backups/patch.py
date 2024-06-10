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
"""Update the expiry time of the FINAL backup."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.sql import api_util
from googlecloudsdk.api_lib.sql import operations
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.sql import flags
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


@base.Hidden
@base.ReleaseTracks(
    base.ReleaseTrack.GA, base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA
)
class Patch(base.UpdateCommand):
  """Update the Final backup of a Cloud SQL project."""

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Args:
      parser: An argparse parser that you can use to add arguments that go on
        the command line after this command. Positional arguments are allowed.
    """
    flags.AddBackupName(parser)
    expiration = parser.add_mutually_exclusive_group(required=True, hidden=True)
    flags.AddBackupExpiryTime(expiration)
    flags.AddBackupTtlDays(expiration)

  def Run(self, args):
    """Update the Final backup of a Cloud SQL project.

    Args:
      args: argparse.Namespace, The arguments that this command was invoked
        with.

    Returns:
      A dict object representing the operations resource describing the delete
      operation if the api request was successful.
    """

    client = api_util.SqlClient(api_util.API_VERSION_DEFAULT)
    sql_client = client.sql_client
    sql_messages = client.sql_messages

    console_io.PromptContinue(
        message="This backup's expiration time is updated.",
        default=True,
        cancel_on_no=True,
    )
    patch_backup = sql_messages.Backup(
        name=args.name,
    )
    update_mask = None
    if args.ttl_days is not None and args.ttl_days > 0:
      patch_backup.ttlDays = args.ttl_days
      update_mask = 'ttl_days'

    if args.expiry_time is not None:
      patch_backup.expiryTime = args.expiry_time.strftime(
          '%Y-%m-%dT%H:%M:%S.%fZ')
      update_mask = 'expiry_time'

    request = sql_messages.SqlBackupsUpdateBackupRequest(
        backup=patch_backup,
        name=args.name,
        updateMask=update_mask,
    )
    result = sql_client.backups.UpdateBackup(request)
    operation_ref = client.resource_parser.Create(
        'sql.operations', operation=result.name, project=args.name.split('/')[1]
    )

    operations.OperationsV1Beta4.WaitForOperation(
        sql_client, operation_ref, 'Updating backup'
    )

    log.UpdatedResource(args.name)
