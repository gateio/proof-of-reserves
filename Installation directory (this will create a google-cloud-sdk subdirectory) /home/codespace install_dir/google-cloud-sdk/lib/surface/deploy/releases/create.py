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
"""Create a release."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime
import os.path

from apitools.base.py import exceptions as apitools_exceptions
from googlecloudsdk.api_lib.clouddeploy import client_util
from googlecloudsdk.api_lib.clouddeploy import config
from googlecloudsdk.api_lib.clouddeploy import release
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions as c_exceptions
from googlecloudsdk.command_lib.deploy import delivery_pipeline_util
from googlecloudsdk.command_lib.deploy import deploy_policy_util
from googlecloudsdk.command_lib.deploy import deploy_util
from googlecloudsdk.command_lib.deploy import flags
from googlecloudsdk.command_lib.deploy import promote_util
from googlecloudsdk.command_lib.deploy import release_util
from googlecloudsdk.command_lib.deploy import resource_args
from googlecloudsdk.core import exceptions as core_exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core import resources
from googlecloudsdk.core.util import files
from googlecloudsdk.core.util import times


_DETAILED_HELP = {
    'DESCRIPTION': '{description}',
    'EXAMPLES': """ \
    To create a release with source located at storage URL `gs://bucket/object.zip`
    and the first rollout in the first target of the promotion sequence:

       $ {command} my-release --source=`gs://bucket/object.zip` --delivery-pipeline=my-pipeline --region=us-central1

    To create a release with source located at current directory
    and deploy a rollout to target prod :

      $ {command} my-release --delivery-pipeline=my-pipeline --region=us-central1 --to-target=prod

    The following command creates a release without a `skaffold.yaml` as input, and generates one
    for you:

      $ {command} my-release --delivery-pipeline=my-pipeline --region=us-central1 --from-k8s-manifest=path/to/kubernetes/k8.yaml

    The current UTC date and time on the machine running the gcloud command can
    also be included in the release name by adding $DATE and $TIME parameters:

      $ {command} 'my-release-$DATE-$TIME' --delivery-pipeline=my-pipeline --region=us-central1

    If the current UTC date and time is set to 2021-12-21 12:02, then the created release
    will have its name set as my-release-20211221-1202.

    When using these parameters, please be sure to wrap the release name in single quotes
    or else the template parameters will be overridden by environment variables.
    """,
}
_RELEASE = 'release'


def _CommonArgs(parser):
  """Register flags for this command.

  Args:
    parser: An argparse.ArgumentParser-like object. It is mocked out in order to
      capture some information, but behaves like an ArgumentParser.
  """
  resource_args.AddReleaseResourceArg(parser, positional=True, required=True)
  flags.AddGcsSourceStagingDirFlag(parser)
  flags.AddImagesGroup(parser)
  flags.AddIgnoreFileFlag(parser)
  flags.AddToTargetFlag(parser)
  flags.AddDescription(parser, 'Description of the release.')
  flags.AddAnnotationsFlag(parser, _RELEASE)
  flags.AddLabelsFlag(parser, _RELEASE)
  flags.AddSkaffoldVersion(parser)
  flags.AddSkaffoldSources(parser)
  flags.AddInitialRolloutGroup(parser)
  flags.AddDeployParametersFlag(parser)
  flags.AddOverrideDeployPolicies(parser)


@base.ReleaseTracks(
    base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA, base.ReleaseTrack.GA
)
class Create(base.CreateCommand):
  """Creates a new release, delivery pipeline qualified."""

  detailed_help = _DETAILED_HELP

  @staticmethod
  def Args(parser):
    _CommonArgs(parser)

  def _CheckSupportedVersion(self, release_ref, skaffold_version):
    config_client = config.ConfigClient()
    try:
      c = config_client.GetConfig(
          release_ref.AsDict()['projectsId'],
          release_ref.AsDict()['locationsId'],
      )
    except apitools_exceptions.HttpForbiddenError:
      # We can't display any preemptive warnings, but the server will still
      # prevent any mischief later.
      return

    version_obj = None
    for v in c.supportedVersions:
      if v.version == skaffold_version:
        version_obj = v
        break
    if not version_obj:
      return

    try:
      maintenance_dt = times.ParseDateTime(version_obj.maintenanceModeTime)
    except (times.DateTimeSyntaxError, times.DateTimeValueError):
      maintenance_dt = None
    try:
      support_expiration_dt = times.ParseDateTime(
          version_obj.supportExpirationTime
      )
    except (times.DateTimeSyntaxError, times.DateTimeValueError):
      support_expiration_dt = None
    if maintenance_dt and (
        maintenance_dt - times.Now()) <= datetime.timedelta(days=28):
      log.status.Print(
          'WARNING: This release\'s Skaffold version will be'
          ' in maintenance mode beginning on {date}.'
          ' After that you won\'t be able to create releases'
          ' using this version of Skaffold.\n'
          'https://cloud.google.com/deploy/docs/using-skaffold'
          '/select-skaffold#skaffold_version_deprecation'
          '_and_maintenance_policy'.format(
              date=maintenance_dt.strftime('%Y-%m-%d'))
      )
    if support_expiration_dt and times.Now() > support_expiration_dt:
      raise core_exceptions.Error(
          'The Skaffold version you\'ve chosen is no longer supported.\n'
          'https://cloud.google.com/deploy/docs/using-skaffold/select-skaffold'
          '#skaffold_version_deprecation_and_maintenance_policy'
      )
    if maintenance_dt and times.Now() > maintenance_dt:
      raise core_exceptions.Error(
          'You can\'t create a new release using a Skaffold version'
          ' that is in maintenance mode.\n'
          'https://cloud.google.com/deploy/docs/using-skaffold/select-skaffold'
          '#skaffold_version_deprecation_and_maintenance_policy'
      )

  def Run(self, args):
    """This is what gets called when the user runs this command."""
    if args.disable_initial_rollout and args.to_target:
      raise c_exceptions.ConflictingArgumentsException(
          '--disable-initial-rollout', '--to-target'
      )
    if args.from_run_container:
      if args.build_artifacts:
        raise c_exceptions.ConflictingArgumentsException(
            '--from-run-container',
            '--build-artifacts',
        )
      if args.images:
        raise c_exceptions.ConflictingArgumentsException(
            '--from-run-container',
            '--images'
        )
    args.CONCEPTS.parsed_args.release = release_util.RenderPattern(
        args.CONCEPTS.parsed_args.release
    )
    release_ref = args.CONCEPTS.release.Parse()
    pipeline_obj = delivery_pipeline_util.GetPipeline(
        release_ref.Parent().RelativeName()
    )
    failed_activity_msg = 'Cannot create release {}.'.format(
        release_ref.RelativeName()
    )
    delivery_pipeline_util.ThrowIfPipelineSuspended(
        pipeline_obj, failed_activity_msg
    )

    if args.skaffold_file:
      # Only when skaffold is absolute path need to be handled here
      if os.path.isabs(args.skaffold_file):
        if args.source == '.':
          source = os.getcwd()
          source_description = 'current working directory'
        else:
          source = args.source
          source_description = 'source'
        if not files.IsDirAncestorOf(source, args.skaffold_file):
          raise core_exceptions.Error(
              'The skaffold file {} could not be found in the {}. Please enter'
              ' a valid Skaffold file path.'.format(
                  args.skaffold_file, source_description
              )
          )
        args.skaffold_file = os.path.relpath(
            os.path.abspath(args.skaffold_file), os.path.abspath(source)
        )
    if args.skaffold_version:
      self._CheckSupportedVersion(release_ref, args.skaffold_version)

    client = release.ReleaseClient()
    # Create the release create request.
    release_config = release_util.CreateReleaseConfig(
        args.source,
        args.gcs_source_staging_dir,
        args.ignore_file,
        args.images,
        args.build_artifacts,
        args.description,
        args.skaffold_version,
        args.skaffold_file,
        release_ref.AsDict()['locationsId'],
        pipeline_obj.uid,
        args.from_k8s_manifest,
        args.from_run_manifest,
        args.from_run_container,
        args.services,
        pipeline_obj,
        args.deploy_parameters,
    )

    deploy_util.SetMetadata(
        client.messages,
        release_config,
        deploy_util.ResourceType.RELEASE,
        args.annotations,
        args.labels,
    )
    operation = client.Create(release_ref, release_config)
    operation_ref = resources.REGISTRY.ParseRelativeName(
        operation.name, collection='clouddeploy.projects.locations.operations'
    )
    client_util.OperationsClient().WaitForOperation(operation, operation_ref)

    log.status.Print(
        'Created Cloud Deploy release {}.'.format(release_ref.Name())
    )

    release_obj = release.ReleaseClient().Get(release_ref.RelativeName())
    if args.disable_initial_rollout:
      return release_obj
    # On the command line deploy policy IDs are provided, but for the
    # CreateRollout API we need to provide the full resource name.
    pipeline_ref = release_ref.Parent()
    policies = deploy_policy_util.CreateDeployPolicyNamesFromIDs(
        pipeline_ref, args.override_deploy_policies
    )
    rollout_resource = promote_util.Promote(
        release_ref,
        release_obj,
        args.to_target,
        is_create=True,
        labels=args.initial_rollout_labels,
        annotations=args.initial_rollout_annotations,
        starting_phase_id=args.initial_rollout_phase_id,
        override_deploy_policies=policies,
    )

    return release_obj, rollout_resource
