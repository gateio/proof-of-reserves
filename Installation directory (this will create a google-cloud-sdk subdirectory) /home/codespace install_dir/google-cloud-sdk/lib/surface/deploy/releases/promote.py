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
"""Promote new Cloud Deploy release."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.clouddeploy import release
from googlecloudsdk.api_lib.util import apis as core_apis
from googlecloudsdk.api_lib.util import exceptions as gcloud_exception
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.deploy import delivery_pipeline_util
from googlecloudsdk.command_lib.deploy import deploy_policy_util
from googlecloudsdk.command_lib.deploy import exceptions as deploy_exceptions
from googlecloudsdk.command_lib.deploy import flags
from googlecloudsdk.command_lib.deploy import promote_util
from googlecloudsdk.command_lib.deploy import release_util
from googlecloudsdk.command_lib.deploy import resource_args
from googlecloudsdk.core import exceptions as core_exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


_DETAILED_HELP = {
    'DESCRIPTION': '{description}',
    'EXAMPLES': """ \
  To promote a release called 'test-release' for delivery pipeline 'test-pipeline' in region 'us-central1' to target 'prod', run:

  $ {command} --release=test-release --delivery-pipeline=test-pipeline --region=us-central1 --to-target=prod


""",
}
_ROLLOUT = 'rollout'


def _CommonArgs(parser):
  """Register flags for this command.

  Args:
    parser: An argparse.ArgumentParser-like object. It is mocked out in order to
      capture some information, but behaves like an ArgumentParser.
  """
  resource_args.AddReleaseResourceArg(parser)
  flags.AddToTarget(parser)
  flags.AddRolloutID(parser)
  flags.AddAnnotationsFlag(parser, _ROLLOUT)
  flags.AddLabelsFlag(parser, _ROLLOUT)
  flags.AddStartingPhaseId(parser)
  flags.AddOverrideDeployPolicies(parser)


@base.ReleaseTracks(
    base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA, base.ReleaseTrack.GA
)
class Promote(base.CreateCommand):
  """Promotes a release from one target (source), to another (destination).

  If to-target is not specified the command promotes the release from the target
  that is farthest along in the promotion sequence to its next stage in the
  promotion sequence.
  """

  detailed_help = _DETAILED_HELP

  @staticmethod
  def Args(parser):
    _CommonArgs(parser)

  @gcloud_exception.CatchHTTPErrorRaiseHTTPException(
      deploy_exceptions.HTTP_ERROR_FORMAT
  )
  def Run(self, args):
    release_ref = args.CONCEPTS.release.Parse()
    pipeline_ref = release_ref.Parent()
    pipeline_obj = delivery_pipeline_util.GetPipeline(
        pipeline_ref.RelativeName()
    )
    failed_activity_msg = 'Cannot promote release {}.'.format(
        release_ref.RelativeName()
    )
    delivery_pipeline_util.ThrowIfPipelineSuspended(
        pipeline_obj, failed_activity_msg
    )
    release_obj = release.ReleaseClient().Get(release_ref.RelativeName())

    messages = core_apis.GetMessagesModule('clouddeploy', 'v1')
    skaffold_support_state = release_util.GetSkaffoldSupportState(release_obj)
    skaffold_support_state_enum = (
        messages.SkaffoldSupportedCondition.SkaffoldSupportStateValueValuesEnum
    )
    if (skaffold_support_state ==
        skaffold_support_state_enum.SKAFFOLD_SUPPORT_STATE_MAINTENANCE_MODE):
      log.status.Print(
          "WARNING: This release's Skaffold version is in maintenance mode and"
          " will be unsupported soon.\n"
          " https://cloud.google.com/deploy/docs/using-skaffold/select-skaffold"
          "#skaffold_version_deprecation_and_maintenance_policy")

    if (skaffold_support_state ==
        skaffold_support_state_enum.SKAFFOLD_SUPPORT_STATE_UNSUPPORTED):
      raise core_exceptions.Error(
          "You can't promote this release because the Skaffold version that was"
          " used to create the release is no longer supported.\n"
          "https://cloud.google.com/deploy/docs/using-skaffold/select-skaffold"
          "#skaffold_version_deprecation_and_maintenance_policy"
      )

    if release_obj.abandoned:
      raise deploy_exceptions.AbandonedReleaseError(
          'Cannot promote release.', release_ref.RelativeName()
      )

    # Get the to_target id if the argument is not specified.
    to_target_id = args.to_target
    if not to_target_id:
      to_target_id = promote_util.GetToTargetID(release_obj, False)

      # If there are any rollouts in progress for the given release, and no
      # to-target was given throw an exception.
      promote_util.CheckIfInProgressRollout(
          release_ref, release_obj, to_target_id
      )

    release_util.PrintDiff(release_ref, release_obj, args.to_target)

    console_io.PromptContinue(
        'Promoting release {} to target {}.'.format(
            release_ref.Name(), to_target_id
        ),
        cancel_on_no=True,
    )
    # On the command line deploy policy IDs are provided, but for the
    # CreateRollout API we need to provide the full resource name.
    policies = deploy_policy_util.CreateDeployPolicyNamesFromIDs(
        pipeline_ref, args.override_deploy_policies
    )
    rollout_resource = promote_util.Promote(
        release_ref,
        release_obj,
        to_target_id,
        False,
        rollout_id=args.rollout_id,
        annotations=args.annotations,
        labels=args.labels,
        starting_phase_id=args.starting_phase_id,
        override_deploy_policies=policies,
    )
    return rollout_resource
