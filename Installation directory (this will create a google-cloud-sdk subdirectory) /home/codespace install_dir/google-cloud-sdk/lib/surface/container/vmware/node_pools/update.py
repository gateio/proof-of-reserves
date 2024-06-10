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
"""Command to update a node pool in an Anthos cluster on VMware."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.container.gkeonprem import operations
from googlecloudsdk.api_lib.container.gkeonprem import vmware_node_pools as apis
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import parser_arguments
from googlecloudsdk.command_lib.container.gkeonprem import constants
from googlecloudsdk.command_lib.container.vmware import constants as vmware_constants
from googlecloudsdk.command_lib.container.vmware import flags
from googlecloudsdk.core import log

_EXAMPLES = """
To update a node pool named ``my-node-pool'' in a cluster named
``my-cluster'' managed in location ``us-west1'', run:

$ {command} my-node-pool --cluster=my-cluster --location=us-west1
"""


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class UpdateAlpha(base.UpdateCommand):
  """Update a node pool in an Anthos cluster on VMware."""

  detailed_help = {'EXAMPLES': _EXAMPLES}

  @staticmethod
  def Args(parser: parser_arguments.ArgumentInterceptor):
    """Gathers commandline arguments for the update command.

    Args:
      parser: The argparse parser to add the flag to.
    """
    parser.display_info.AddFormat(vmware_constants.VMWARE_NODEPOOLS_FORMAT)
    flags.AddNodePoolResourceArg(parser, 'to update')
    flags.AddValidationOnly(parser)
    base.ASYNC_FLAG.AddToParser(parser)
    flags.AddNodePoolDisplayName(parser)
    flags.AddVmwareNodePoolAutoscalingConfig(parser, for_update=True)
    flags.AddVmwareNodeConfig(parser, for_update=True)
    flags.AddNodePoolVersion(parser)

  def Run(self, args):
    """Runs the update command.

    Args:
      args: The arguments received from command line.

    Returns:
      The return value depends on the command arguments. If `--async` is
      specified, it returns an operation; otherwise, it returns the updated
      resource. If `--validate-only` is specified, it returns None or any
      possible error.
    """
    node_pool_ref = args.CONCEPTS.node_pool.Parse()
    client = apis.NodePoolsClient()
    operation = client.Update(args)

    if args.async_ and not args.IsSpecified('format'):
      args.format = constants.OPERATIONS_FORMAT

    if args.validate_only:
      return

    if args.async_:
      log.UpdatedResource(
          node_pool_ref, 'Node Pool in Anthos Cluster on VMware', args.async_
      )
      return operation
    else:
      operation_client = operations.OperationsClient()
      response = operation_client.Wait(operation)
      log.UpdatedResource(
          node_pool_ref, 'Node Pool in Anthos Cluster on VMware', args.async_
      )
      return response


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class UpdateBeta(base.UpdateCommand):
  """Update a node pool in an Anthos cluster on VMware."""

  detailed_help = {'EXAMPLES': _EXAMPLES}

  @staticmethod
  def Args(parser: parser_arguments.ArgumentInterceptor):
    """Gathers commandline arguments for the update command.

    Args:
      parser: The argparse parser to add the flag to.
    """
    parser.display_info.AddFormat(vmware_constants.VMWARE_NODEPOOLS_FORMAT)
    flags.AddNodePoolResourceArg(parser, 'to update')
    flags.AddValidationOnly(parser)
    base.ASYNC_FLAG.AddToParser(parser)
    flags.AddNodePoolDisplayName(parser)
    flags.AddVmwareNodePoolAutoscalingConfig(parser, for_update=True)
    flags.AddVmwareNodeConfig(parser, for_update=True)
    flags.AddNodePoolVersion(parser)

  def Run(self, args):
    """Runs the update command.

    Args:
      args: The arguments received from command line.

    Returns:
      The return value depends on the command arguments. If `--async` is
      specified, it returns an operation; otherwise, it returns the updated
      resource. If `--validate-only` is specified, it returns None or any
      possible error.
    """
    node_pool_ref = args.CONCEPTS.node_pool.Parse()
    client = apis.NodePoolsClient()
    operation = client.Update(args)

    if args.async_ and not args.IsSpecified('format'):
      args.format = constants.OPERATIONS_FORMAT

    if args.validate_only:
      return

    if args.async_:
      log.UpdatedResource(
          node_pool_ref, 'Node Pool in Anthos Cluster on VMware', args.async_
      )
      return operation
    else:
      operation_client = operations.OperationsClient()
      response = operation_client.Wait(operation)
      log.UpdatedResource(
          node_pool_ref, 'Node Pool in Anthos Cluster on VMware', args.async_
      )
      return response


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Update(base.UpdateCommand):
  """Update a node pool in an Anthos cluster on VMware."""

  detailed_help = {'EXAMPLES': _EXAMPLES}

  @staticmethod
  def Args(parser: parser_arguments.ArgumentInterceptor):
    """Gathers commandline arguments for the update command.

    Args:
      parser: The argparse parser to add the flag to.
    """
    parser.display_info.AddFormat(vmware_constants.VMWARE_NODEPOOLS_FORMAT)
    flags.AddNodePoolResourceArg(parser, 'to update')
    flags.AddValidationOnly(parser)
    base.ASYNC_FLAG.AddToParser(parser)
    flags.AddNodePoolDisplayName(parser)
    flags.AddVmwareNodePoolAutoscalingConfig(parser, for_update=True)
    flags.AddVmwareNodeConfig(parser, for_update=True)
    flags.AddNodePoolVersion(parser)

  def Run(self, args):
    """Runs the update command.

    Args:
      args: The arguments received from command line.

    Returns:
      The return value depends on the command arguments. If `--async` is
      specified, it returns an operation; otherwise, it returns the updated
      resource. If `--validate-only` is specified, it returns None or any
      possible error.
    """
    node_pool_ref = args.CONCEPTS.node_pool.Parse()
    client = apis.NodePoolsClient()
    operation = client.Update(args)

    if args.async_ and not args.IsSpecified('format'):
      args.format = constants.OPERATIONS_FORMAT

    if args.validate_only:
      return

    if args.async_:
      log.UpdatedResource(
          node_pool_ref, 'Node Pool in Anthos Cluster on VMware', args.async_
      )
      return operation
    else:
      operation_client = operations.OperationsClient()
      response = operation_client.Wait(operation)
      log.UpdatedResource(
          node_pool_ref, 'Node Pool in Anthos Cluster on VMware', args.async_
      )
      return response
