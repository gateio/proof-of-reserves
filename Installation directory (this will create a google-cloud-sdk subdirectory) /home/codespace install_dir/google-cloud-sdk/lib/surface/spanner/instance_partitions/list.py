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
"""Command for spanner instance partitions list."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import textwrap

from googlecloudsdk.api_lib.spanner import instance_partitions
from googlecloudsdk.calliope import base
# from googlecloudsdk.command_lib.spanner import flags
from googlecloudsdk.command_lib.spanner import resource_args


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class AlphaList(base.ListCommand):
  """List the Cloud Spanner instance partitions contained within the given instance with ALPHA features."""

  detailed_help = {
      'EXAMPLES': textwrap.dedent("""\
      To list all Cloud Spanner instances partitions in an instance, run:

      $ {command} --instance=my-instance-id
      """),
  }

  @staticmethod
  def Args(parser):
    resource_args.AddInstanceResourceArg(
        parser, 'in which to list instance partitions', positional=False
    )
    base.FILTER_FLAG.RemoveFromParser(parser)  # we don't support filter
    parser.display_info.AddFormat("""
          table(
            name.basename(),
            displayName,
            config.basename(),
            nodeCount,
            processing_units,
            state
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
    return instance_partitions.List(args.CONCEPTS.instance.Parse())
