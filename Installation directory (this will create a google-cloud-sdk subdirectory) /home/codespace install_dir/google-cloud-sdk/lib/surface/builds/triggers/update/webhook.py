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
"""Update Webhook trigger command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import textwrap

from googlecloudsdk.api_lib.cloudbuild import cloudbuild_util
from googlecloudsdk.api_lib.cloudbuild import trigger_config as trigger_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.cloudbuild import resource_args
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources


class UpdateWebhook(base.UpdateCommand):
  """Update a Webhook trigger used by Cloud Build."""

  detailed_help = {
      'EXAMPLES': textwrap.dedent("""\
            To update the branch from which the trigger clones:

              $ {command} my-webhook-trigger --source-to-build-branch=my-branch

            To update the webhook secret:

              $ {command} my-webhook-trigger --secret=projects/my-project/secrets/my-secret/versions/2

            To update the substitutions of the trigger:
              $ {command} my-trigger --update-substitutions=_REPO_NAME=my-repo,_BRANCH_NAME=master
          """),
  }

  @staticmethod
  def Args(parser):
    """Register flags for this command.

    Args:
      parser: An argparse.ArgumentParser-like object. It is mocked out in order
        to capture some information, but behaves like an ArgumentParser.
    """
    concept_parsers.ConceptParser.ForResource(
        'TRIGGER',
        resource_args.GetTriggerResourceSpec(),
        'Build Trigger.',
        required=True,
    ).AddToParser(parser)

    flag_config = trigger_utils.AddTriggerArgs(
        parser, add_region_flag=False, add_name=False
    )
    flag_config.add_argument(
        '--secret',
        help=textwrap.dedent("""
            The full path of the secret version required to validate webhook requests against this trigger.
            For example, projects/my-project/secrets/my-secret/versions/1.
        """),
    )
    trigger_utils.AddBuildConfigArgsForUpdate(
        flag_config, has_file_source=True, require_docker_image=False
    )
    trigger_utils.AddRepoSourceForUpdate(flag_config)
    trigger_utils.AddFilterArg(flag_config)

  def ParseTriggerFromFlags(self, args, old_trigger, update_mask):
    """Parses arguments into a build trigger.

    Args:
      args: An argparse arguments object.
      old_trigger: The existing trigger to be updated.
      update_mask: The fields to be updated.

    Returns:
      A build trigger object.
    """
    messages = cloudbuild_util.GetMessagesModule()

    trigger, done = trigger_utils.ParseTriggerArgsForUpdate(args, messages)
    if done:
      return trigger

    project = properties.VALUES.core.project.Get(required=True)
    default_image = 'gcr.io/%s/gcb-%s:$COMMIT_SHA' % (project, args.TRIGGER)
    trigger_utils.ParseBuildConfigArgsForUpdate(
        trigger,
        old_trigger,
        args,
        messages,
        update_mask,
        default_image=default_image,
        has_repo_source=True,
        has_file_source=True,
    )

    trigger.filter = args.subscription_filter

    return trigger

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: An argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      The updated webhook trigger.
    """

    client = cloudbuild_util.GetClientInstance()
    messages = cloudbuild_util.GetMessagesModule()
    project = properties.VALUES.core.project.Get(required=True)
    regionprop = properties.VALUES.builds.region.Get()
    location = args.region or regionprop or cloudbuild_util.DEFAULT_REGION
    triggerid = args.TRIGGER

    name = resources.REGISTRY.Parse(
        triggerid,
        params={
            'projectsId': project,
            'locationsId': location,
            'triggersId': triggerid,
        },
        collection='cloudbuild.projects.locations.triggers',
    ).RelativeName()

    old_trigger = client.projects_locations_triggers.Get(
        client.MESSAGES_MODULE.CloudbuildProjectsLocationsTriggersGetRequest(
            name=name, triggerId=triggerid
        )
    )

    update_mask = []
    trigger = self.ParseTriggerFromFlags(args, old_trigger, update_mask)
    trigger.webhookConfig = messages.WebhookConfig(secret=args.secret)

    # Overwrite the substitutions.additionalProperties in updateMask.
    sub = 'substitutions'
    update_mask.extend(cloudbuild_util.MessageToFieldPaths(trigger))
    update_mask = sorted(
        set(sub if m.startswith(sub) else m for m in update_mask)
    )

    req = messages.CloudbuildProjectsLocationsTriggersPatchRequest(
        resourceName=name,
        triggerId=triggerid,
        buildTrigger=trigger,
        updateMask=','.join(update_mask),
    )

    updated_trigger = client.projects_locations_triggers.Patch(req)
    log.UpdatedResource(triggerid, kind='build_trigger')

    return updated_trigger
