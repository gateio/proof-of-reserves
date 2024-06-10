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
"""Command to delete an Anthos cluster on AWS."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.container.gkemulticloud import aws as api_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.container.aws import resource_args
from googlecloudsdk.command_lib.container.gkemulticloud import command_util
from googlecloudsdk.command_lib.container.gkemulticloud import constants
from googlecloudsdk.command_lib.container.gkemulticloud import endpoint_util
from googlecloudsdk.command_lib.container.gkemulticloud import flags

_EXAMPLES = """
To delete a cluster named ``my-cluster'' managed in location ``us-west1'',
run:

$ {command} my-cluster --location=us-west1
"""


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.GA)
class Delete(base.DeleteCommand):
  """Delete an Anthos cluster on AWS."""

  detailed_help = {'EXAMPLES': _EXAMPLES}

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    resource_args.AddAwsClusterResourceArg(parser, 'to delete')

    flags.AddValidateOnly(parser, 'cluster to delete')
    flags.AddAllowMissing(parser, 'cluster')
    flags.AddIgnoreErrors(parser, constants.AWS, 'cluster')

    base.ASYNC_FLAG.AddToParser(parser)

  def Run(self, args):
    """Runs the delete command."""
    location = resource_args.ParseAwsClusterResourceArg(args).locationsId
    with endpoint_util.GkemulticloudEndpointOverride(location):
      cluster_ref = resource_args.ParseAwsClusterResourceArg(args)
      cluster_client = api_util.ClustersClient()
      cluster = cluster_client.Get(cluster_ref)
      message = command_util.ClusterMessage(
          cluster_ref.awsClustersId,
          kind=constants.AWS,
          region=cluster.awsRegion,
      )
      command_util.DeleteWithIgnoreErrors(
          args,
          cluster_client,
          cluster_ref,
          message,
          constants.AWS_CLUSTER_KIND,
      )
