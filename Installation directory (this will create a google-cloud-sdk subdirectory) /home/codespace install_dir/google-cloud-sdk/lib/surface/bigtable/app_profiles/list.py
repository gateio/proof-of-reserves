# -*- coding: utf-8 -*- #
# Copyright 2018 Google LLC. All Rights Reserved.
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
"""bigtable app profiles list command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import textwrap

from googlecloudsdk.api_lib.bigtable import app_profiles
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.bigtable import arguments


def _TransformAppProfileToRoutingInfo(app_profile):
  """Extracts the routing info from the app profile."""
  if ('singleClusterRouting' in app_profile and
      'clusterId' in app_profile['singleClusterRouting']):
    return app_profile['singleClusterRouting']['clusterId']
  elif 'multiClusterRoutingUseAny' in app_profile:
    if 'clusterIds' in app_profile['multiClusterRoutingUseAny']:
      return ','.join(app_profile['multiClusterRoutingUseAny']['clusterIds'])
    return 'MULTI_CLUSTER_USE_ANY'
  return ''


def _TransformAppProfileToFailoverRadius(app_profile):
  """Extracts the failover radius from the app profile."""
  if 'multiClusterRoutingUseAny' in app_profile:
    if 'failoverRadius' in app_profile['multiClusterRoutingUseAny']:
      return app_profile['multiClusterRoutingUseAny']['failoverRadius']
  return ''


def _TransformAppProfileToIsolationMode(app_profile):
  """Extracts the isolation mode from the app profile."""
  if 'dataBoostIsolationReadOnly' in app_profile:
    return 'DATA_BOOST_ISOLATION_READ_ONLY'
  return 'STANDARD_ISOLATION'


def _TransformAppProfileToStandardIsolationPriority(app_profile):
  """Extracts the Data Boot compute billing owner from the app profile."""
  if 'dataBoostIsolationReadOnly' in app_profile:
    return ''
  elif (
      'standardIsolation' in app_profile
      and 'priority' in app_profile['standardIsolation']
  ):
    return app_profile['standardIsolation']['priority']
  else:
    return 'PRIORITY_HIGH'


def _TransformAppProfileToDataBoostComputeBillingOwner(app_profile):
  """Extracts the Data Boot compute billing owner from the app profile."""
  if (
      'dataBoostIsolationReadOnly' in app_profile
      and 'computeBillingOwner' in app_profile['dataBoostIsolationReadOnly']
  ):
    return app_profile['dataBoostIsolationReadOnly']['computeBillingOwner']
  else:
    return ''


@base.ReleaseTracks(base.ReleaseTrack.GA)
class ListAppProfilesGA(base.ListCommand):
  """List Bigtable app profiles."""

  detailed_help = {
      'EXAMPLES':
          textwrap.dedent("""\
          To list all app profiles for an instance, run:

            $ {command} --instance=my-instance-id

          """),
  }

  @staticmethod
  def Args(parser):
    arguments.AddInstanceResourceArg(parser, 'to list app profiles for')

    parser.display_info.AddTransforms({
        'routingInfo': _TransformAppProfileToRoutingInfo,
    })

    # ROUTING is a oneof SingleClusterRouting, MultiClusterRoutingUseAny.
    # Combine into a single ROUTING column in the table.
    parser.display_info.AddFormat("""
          table(
            name.basename():sort=1,
            description:wrap,
            routingInfo():wrap:label=ROUTING,
            singleClusterRouting.allowTransactionalWrites.yesno("Yes"):label=TRANSACTIONAL_WRITES
          )
        """)

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      Some value that we want to have printed later.
    """
    instance_ref = args.CONCEPTS.instance.Parse()
    return app_profiles.List(instance_ref)


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class ListAppProfilesBeta(ListAppProfilesGA):
  """List Bigtable app profiles."""

  @staticmethod
  def Args(parser):
    arguments.AddInstanceResourceArg(parser, 'to list app profiles for')

    parser.display_info.AddTransforms({
        'routingInfo': _TransformAppProfileToRoutingInfo,
        'isolationMode': _TransformAppProfileToIsolationMode,
        'standardIsolationPriority': (
            _TransformAppProfileToStandardIsolationPriority
        ),
        'dataBoostComputeBillingOwner': (
            _TransformAppProfileToDataBoostComputeBillingOwner
        ),
    })

    # ROUTING is a oneof SingleClusterRouting, MultiClusterRoutingUseAny.
    # Combine into a single ROUTING column in the table.
    parser.display_info.AddFormat("""
          table(
            name.basename():sort=1,
            description:wrap,
            routingInfo():wrap:label=ROUTING,
            singleClusterRouting.allowTransactionalWrites.yesno("Yes"):label=TRANSACTIONAL_WRITES,
            isolationMode():label=ISOLATION_MODE,
            standardIsolationPriority():label=STANDARD_ISOLATION_PRIORITY,
            dataBoostComputeBillingOwner():label=DATA_BOOST_COMPUTE_BILLING_OWNER
          )
        """)


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class ListAppProfilesAlpha(ListAppProfilesBeta):
  """List Bigtable app profiles."""

  @staticmethod
  def Args(parser):
    arguments.AddInstanceResourceArg(parser, 'to list app profiles for')

    parser.display_info.AddTransforms({
        'routingInfo': _TransformAppProfileToRoutingInfo,
        'isolationMode': _TransformAppProfileToIsolationMode,
        'standardIsolationPriority': (
            _TransformAppProfileToStandardIsolationPriority
        ),
        'dataBoostComputeBillingOwner': (
            _TransformAppProfileToDataBoostComputeBillingOwner
        ),
        'failoverRadius': _TransformAppProfileToFailoverRadius,
    })

    # ROUTING is a oneof SingleClusterRouting, MultiClusterRoutingUseAny.
    # Combine into a single ROUTING column in the table.
    parser.display_info.AddFormat("""
          table(
            name.basename():sort=1,
            description:wrap,
            routingInfo():wrap:label=ROUTING,
            singleClusterRouting.allowTransactionalWrites.yesno("Yes"):label=TRANSACTIONAL_WRITES,
            isolationMode():label=ISOLATION_MODE,
            standardIsolationPriority():label=STANDARD_ISOLATION_PRIORITY,
            dataBoostComputeBillingOwner():label=DATA_BOOST_COMPUTE_BILLING_OWNER,
            failoverRadius():label=FAILOVER_RADIUS
          )
        """)
