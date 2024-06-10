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
"""Command to delete a fleet namespace."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.container.fleet import client
from googlecloudsdk.api_lib.container.fleet import util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.container.fleet import resources


class Delete(base.DeleteCommand):
  """Delete a fleet namespace.

  This command can fail for the following reasons:
  * The project specified does not exist.
  * The namespace specified does not exist.
  * The caller does not have permission to access the given project or
  namespace.

  ## EXAMPLES

  To delete fleet namespace `NAMESPACE` in the active project:

    $ {command} NAMESPACE

  To delete fleet namespace `NAMESPACE` in project `PROJECT_ID`:

    $ {command} NAMESPACE --project=PROJECT_ID
  """

  @classmethod
  def Args(cls, parser):
    resources.AddScopeNamespaceResourceArg(
        parser,
        api_version=util.VERSION_MAP[cls.ReleaseTrack()],
        namespace_help='Name of the fleet namespace to be deleted.',
        required=True,
    )

  def Run(self, args):
    namespace_arg = args.CONCEPTS.namespace.Parse()
    namespace_path = namespace_arg.RelativeName()
    fleetclient = client.FleetClient(release_track=self.ReleaseTrack())
    return fleetclient.DeleteScopeNamespace(namespace_path)
