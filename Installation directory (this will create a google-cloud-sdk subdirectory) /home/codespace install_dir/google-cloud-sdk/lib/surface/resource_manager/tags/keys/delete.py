# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
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
"""Delete command for the resource manager - Tag Keys CLI."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.resource_manager import tags
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.resource_manager import operations
from googlecloudsdk.command_lib.resource_manager import tag_arguments as arguments
from googlecloudsdk.command_lib.resource_manager import tag_utils


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA,
                    base.ReleaseTrack.GA)
class Delete(base.Command):
  """Deletes the specified TagKey resource.

    Deletes the TagKey resource given the TagKey's parent and short name
    or the TagKey's numeric id.
  """

  detailed_help = {
      'EXAMPLES':
          """
          To delete a TagKey with id ``123'', run:

            $ {command} tagKeys/123

          To delete a TagKey named ``env'' under organization ``456'',
          run:

            $ {command} 456/env
          """
  }

  @staticmethod
  def Args(parser):
    arguments.AddResourceNameArgToParser(parser)
    arguments.AddAsyncArgToParser(parser)

  def Run(self, args):
    service = tags.TagKeysService()
    messages = tags.TagMessages()

    if args.RESOURCE_NAME.find('tagKeys/') == 0:
      tag_key = args.RESOURCE_NAME
    else:
      tag_key = tag_utils.GetNamespacedResource(
          args.RESOURCE_NAME, tag_utils.TAG_KEYS
      ).name

    delete_request = messages.CloudresourcemanagerTagKeysDeleteRequest(
        name=tag_key)

    op = service.Delete(delete_request)

    if args.async_:
      return op

    return operations.WaitForReturnOperation(
        op, 'Waiting for TagKey [{}] to be deleted'.format(tag_key))
