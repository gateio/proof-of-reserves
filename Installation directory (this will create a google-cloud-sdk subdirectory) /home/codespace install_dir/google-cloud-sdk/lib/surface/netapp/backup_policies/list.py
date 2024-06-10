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
"""Lists Cloud NetApp Volumes Backup Policies."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.netapp.backup_policies import client as backuppolicies_client
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.netapp import flags
from googlecloudsdk.command_lib.netapp.backup_policies import flags as backuppolicies_flags
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class ListBeta(base.ListCommand):
  """List Cloud NetApp Volumes Backup Policies."""

  detailed_help = {
      'DESCRIPTION': """\
          Lists Backup Policies for Cloud NetApp Volumes
          """,
      'EXAMPLES': """\
          The following command lists all Backup Policies in the default netapp/location

              $ {command}

          To list all Backup Policies in a specified location, run:

              $ {command} --location=us-central1
          """,
  }

  _RELEASE_TRACK = base.ReleaseTrack.BETA

  @staticmethod
  def Args(parser):
    concept_parsers.ConceptParser(
        [
            flags.GetResourceListingLocationPresentationSpec(
                'The location in which to list Backup Policies.'
            )
        ]
    ).AddToParser(parser)
    parser.display_info.AddFormat(
        backuppolicies_flags.BACKUP_POLICIES_LIST_FORMAT
    )

  def Run(self, args):
    """Run the list command."""
    # Ensure that project is set before parsing location resource.
    properties.VALUES.core.project.GetOrFail()
    location_ref = args.CONCEPTS.location.Parse().RelativeName()
    # Default to listing all Cloud NetApp Active Directories in all locations.
    location = args.location if args.location else '-'
    location_list = location_ref.split('/')
    location_list[-1] = location
    location_ref = '/'.join(location_list)
    client = backuppolicies_client.BackupPoliciesClient(
        release_track=self._RELEASE_TRACK)
    return list(client.ListBackupPolicies(location_ref, limit=args.limit))

