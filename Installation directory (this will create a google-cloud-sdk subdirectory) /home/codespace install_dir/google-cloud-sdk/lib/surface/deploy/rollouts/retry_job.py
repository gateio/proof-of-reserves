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
"""Retries a Cloud Deploy rollout job specified by job and phase."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.clouddeploy import rollout
from googlecloudsdk.api_lib.util import exceptions as gcloud_exception
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.deploy import delivery_pipeline_util
from googlecloudsdk.command_lib.deploy import deploy_policy_util
from googlecloudsdk.command_lib.deploy import exceptions as deploy_exceptions
from googlecloudsdk.command_lib.deploy import flags
from googlecloudsdk.command_lib.deploy import resource_args
from googlecloudsdk.core import log

_DETAILED_HELP = {
    'DESCRIPTION':
        '{description}',
    'EXAMPLES':
        """ \
    To retry a job 'test-job' in phase 'test-phase' on a rollout 'test-rollout' for delivery pipeline 'test-pipeline', release 'test-release' in region 'us-central1', run:

      $ {command} test-rollout --job-id=test-job --phase-id=test-phase --delivery-pipeline=test-pipeline --release=test-release --region=us-central1

""",
}


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA,
                    base.ReleaseTrack.GA)
class RetryJob(base.CreateCommand):
  """Retries a specified job, phase combination on a rollout."""
  detailed_help = _DETAILED_HELP

  @staticmethod
  def Args(parser):
    resource_args.AddRolloutResourceArg(parser, positional=True)
    flags.AddJobId(parser)
    flags.AddPhaseId(parser)
    flags.AddOverrideDeployPolicies(parser)

  @gcloud_exception.CatchHTTPErrorRaiseHTTPException(
      deploy_exceptions.HTTP_ERROR_FORMAT
  )
  def Run(self, args):
    rollout_ref = args.CONCEPTS.rollout.Parse()
    pipeline_ref = rollout_ref.Parent().Parent()
    pipeline_obj = delivery_pipeline_util.GetPipeline(
        pipeline_ref.RelativeName())
    failed_activity_msg = 'Cannot retry job on rollout {}.'.format(
        rollout_ref.RelativeName())
    delivery_pipeline_util.ThrowIfPipelineSuspended(pipeline_obj,
                                                    failed_activity_msg)

    log.status.Print('Retrying job {} in phase {} of rollout {}.\n'.format(
        args.job_id, args.phase_id, rollout_ref.RelativeName()))
    # On the command line deploy policy IDs are provided, but for the
    # RetryJob API we need to provide the full resource name.
    policies = deploy_policy_util.CreateDeployPolicyNamesFromIDs(
        pipeline_ref, args.override_deploy_policies
    )
    return rollout.RolloutClient().RetryJob(
        rollout_ref.RelativeName(),
        args.job_id,
        args.phase_id,
        override_deploy_policies=policies,
    )
