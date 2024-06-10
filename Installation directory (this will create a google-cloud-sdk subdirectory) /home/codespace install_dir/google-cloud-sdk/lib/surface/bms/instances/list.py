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
"""'Bare Metal Solution instances list command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.bms.bms_client import BmsClient
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.bms import flags
from googlecloudsdk.command_lib.bms import util
from googlecloudsdk.core.resource import resource_projector

DETAILED_HELP = {
    'DESCRIPTION':
        """
          List Bare Metal Solution instances in a project.
        """,
    'EXAMPLES':
        """
          To list instances in the region within the project ``us-central1'', run:

            $ {command} --region=us-central1

          Or:

          To list all instances in the project, run:

            $ {command}
    """,
}


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.GA)
class List(base.ListCommand):
  """List Bare Metal Solution instances in a project."""

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    # Remove unsupported default List flags.
    base.FILTER_FLAG.RemoveFromParser(parser)
    base.PAGE_SIZE_FLAG.RemoveFromParser(parser)
    base.SORT_BY_FLAG.RemoveFromParser(parser)
    base.URI_FLAG.RemoveFromParser(parser)
    flags.FILTER_FLAG_NO_SORTBY_DOC.AddToParser(parser)

    flags.AddRegionArgToParser(parser)
    # The default format picks out the components of the relative name:
    # given projects/myproject/locations/us-central1/instances/my-test
    # it takes -1 (my-test), -3 (us-central1), and -5 (myproject).
    parser.display_info.AddFormat(
        'table(name.segment(-1):label=NAME,id:label=ID,'
        'name.segment(-5):label=PROJECT,'
        'name.segment(-3):label=REGION,machineType,'
        'clientNetworks[].ipAddress.notnull().list():label=CLIENT_IPS,'
        'privateNetworks[].ipAddress.notnull().list():label=PRIVATE_IPS,'
        'state)')

  def Run(self, args):
    region = util.FixParentPathWithGlobalRegion(args.CONCEPTS.region.Parse())
    client = BmsClient()
    for instance in client.ListInstances(region, limit=args.limit):
      synthesized_instance = self.synthesizedInstance(instance, client)
      yield synthesized_instance

  def synthesizedInstance(self, instance, client):
    """Returns a synthesized Instance resource.

    Synthesized Instance has additional lists of networks for client and
    private.

    Args:
      instance: protorpc.messages.Message, The BMS instance.
      client: BmsClient, BMS API client.

    Returns:
      Synthesized Instance resource.

    """
    synthesized_instance = resource_projector.MakeSerializable(instance)
    client_networks = []
    private_networks = []
    for network in instance.networks:
      if client.IsClientNetwork(network):
        client_networks.append(network)
      elif client.IsPrivateNetwork(network):
        private_networks.append(network)

    # If the IPs are not available in networks, look up logical interfaces. This
    # normally would only happen for new multi-vlan customers who use network
    # templates other than the default bondaa-bondaa for their instances.
    if (not client_networks and not private_networks and
       instance.logicalInterfaces):
      for logical_interface in instance.logicalInterfaces:
        for logical_network_interface in logical_interface.logicalNetworkInterfaces:
          if client.IsClientLogicalNetworkInterface(logical_network_interface):
            client_networks.append(logical_network_interface)
          elif client.IsPrivateLogicalNetworkInterface(
              logical_network_interface):
            private_networks.append(logical_network_interface)

    synthesized_instance['clientNetworks'] = client_networks
    synthesized_instance['privateNetworks'] = private_networks
    return synthesized_instance


List.detailed_help = DETAILED_HELP
