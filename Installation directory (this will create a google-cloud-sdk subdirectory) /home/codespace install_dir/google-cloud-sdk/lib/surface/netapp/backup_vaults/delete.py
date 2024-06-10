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
"""Delete a Cloud NetApp Volumes Backup Vault."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.netapp.backup_vaults import client as backupvaults_client
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.netapp.backup_vaults import flags as backupvaults_flags
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class DeleteBeta(base.DeleteCommand):
  """Delete a Cloud NetApp Volumes Backup Vault."""

  detailed_help = {
      'DESCRIPTION': """\
          Delete a Backup Vault.
          """,
      'EXAMPLES': """\
          The following command deletes a Backup Vault instance named BACKUP_VAULT in the default netapp/location:

              $ {command} BACKUP_VAULT

          To delete a Backup Vault named BACKUP_VAULT asynchronously, run the following command:

              $ {command} BACKUP_VAULT --async
          """,
  }

  _RELEASE_TRACK = base.ReleaseTrack.BETA

  @staticmethod
  def Args(parser):
    backupvaults_flags.AddBackupVaultDeleteArgs(parser)

  def Run(self, args):
    """Delete a Cloud NetApp Volumes Backup Vault."""

    backupvault_ref = args.CONCEPTS.backup_vault.Parse()
    if not args.quiet:
      delete_warning = ('You are about to delete a Backup Vault {}.\n'
                        'Are you sure?'.format(backupvault_ref.RelativeName()))
      if not console_io.PromptContinue(message=delete_warning):
        return None
    client = backupvaults_client.BackupVaultsClient(
        release_track=self._RELEASE_TRACK)
    result = client.DeleteBackupVault(backupvault_ref, args.async_)

    if args.async_:
      command = 'gcloud {} netapp backup-vaults list'.format(
          self.ReleaseTrack().prefix)
      log.status.Print(
          'Check the status of the deletion by listing all Backup Vaults:\n  '
          '$ {} '.format(command))
    return result
