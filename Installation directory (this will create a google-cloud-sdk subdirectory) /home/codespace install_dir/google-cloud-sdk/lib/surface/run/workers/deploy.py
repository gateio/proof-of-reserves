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
"""Deploy a container to Cloud Run that will handle workloads that are not ingress based."""

import enum
import os.path
from googlecloudsdk.api_lib.run import api_enabler
from googlecloudsdk.api_lib.run import k8s_object
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions as c_exceptions
from googlecloudsdk.command_lib.artifacts import docker_util
from googlecloudsdk.command_lib.run import artifact_registry
from googlecloudsdk.command_lib.run import config_changes
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import container_parser
from googlecloudsdk.command_lib.run import exceptions
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import messages_util
from googlecloudsdk.command_lib.run import pretty_print
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.run import stages
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io
from googlecloudsdk.core.console import progress_tracker


class BuildType(enum.Enum):
  DOCKERFILE = 'Dockerfile'
  BUILDPACKS = 'Buildpacks'


def ContainerArgGroup():
  """Returns an argument group with all per-container deploy args."""

  help_text = """
Container Flags

  The following flags apply to a single container. If the --container flag is specified these flags may only be
  specified after a --container flag. Otherwise they will apply to the primary container.
"""
  group = base.ArgumentGroup(help=help_text)
  group.AddArgument(flags.SourceAndImageFlags())
  group.AddArgument(flags.MutexEnvVarsFlags())
  group.AddArgument(flags.MemoryFlag())
  group.AddArgument(flags.CpuFlag())
  group.AddArgument(flags.ArgsFlag())
  group.AddArgument(flags.SecretsFlags())
  group.AddArgument(flags.DependsOnFlag())
  group.AddArgument(flags.CommandFlag())
  # ALPHA features
  group.AddArgument(flags.AddVolumeMountFlag())
  group.AddArgument(flags.RemoveVolumeMountFlag())
  group.AddArgument(flags.ClearVolumeMountsFlag())
  group.AddArgument(flags.GpuFlag())

  return group


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Deploy(base.Command):
  """Create or update a Cloud Run worker."""

  detailed_help = {
      'DESCRIPTION': """\
          Creates or updates a Cloud Run worker.
          """,
      'EXAMPLES': """\
          To deploy a container to the worker `my-backend` on Cloud Run:

              $ {command} my-backend --image=us-docker.pkg.dev/project/image

          You may also omit the worker name. Then a prompt will be displayed
          with a suggested default value:

              $ {command} --image=us-docker.pkg.dev/project/image
          """,
  }

  @classmethod
  def Args(cls, parser):
    # Flags specific to managed CR
    managed_group = flags.GetManagedArgGroup(parser)
    flags.AddBinAuthzPolicyFlags(managed_group)
    flags.AddBinAuthzBreakglassFlag(managed_group)
    flags.AddCloudSQLFlags(managed_group)
    flags.AddCmekKeyFlag(managed_group)
    flags.AddCmekKeyRevocationActionTypeFlag(managed_group)
    flags.AddDescriptionFlag(managed_group)
    flags.AddEncryptionKeyShutdownHoursFlag(managed_group)
    flags.AddRevisionSuffixArg(managed_group)
    flags.AddSandboxArg(managed_group)
    flags.RemoveContainersFlag().AddToParser(managed_group)
    flags.AddRuntimeFlag(managed_group)
    flags.AddMinInstancesFlag(managed_group, resource_kind='worker')
    flags.AddVolumesFlags(managed_group, cls.ReleaseTrack())
    flags.AddGpuTypeFlag(managed_group)
    flags.AddVpcNetworkGroupFlagsForUpdate(parser, resource_kind='worker')
    flags.AddEgressSettingsFlag(managed_group)
    flags.SERVICE_MESH_FLAG.AddToParser(managed_group)
    worker_presentation = presentation_specs.ResourcePresentationSpec(
        'WORKER',
        resource_args.GetWorkerResourceSpec(prompt=True),
        'Worker to deploy to.',
        required=True,
        prefixes=False,
    )
    flags.AddAsyncFlag(parser)
    flags.AddLabelsFlags(parser)
    flags.AddGeneralAnnotationFlags(parser)
    flags.AddServiceAccountFlag(parser)
    flags.AddClientNameAndVersionFlags(parser)
    concept_parsers.ConceptParser([worker_presentation]).AddToParser(parser)
    container_args = ContainerArgGroup()
    container_parser.AddContainerFlags(parser, container_args)

    # No output by default, can be overridden by --format
    parser.display_info.AddFormat('none')

  def _ValidateAndGetContainers(self, args):
    if flags.FlagIsExplicitlySet(args, 'containers'):
      containers = args.containers
    else:
      containers = {'': args}

    if len(containers) > 10:
      raise c_exceptions.InvalidArgumentException(
          '--container', 'Workers may include at most 10 containers'
      )
    return containers

  def _ValidateAndGetBuildFromSource(self, containers):
    build_from_source = {
        name: container
        for name, container in containers.items()
        if not container.IsSpecified('image')
    }
    if len(build_from_source) > 1:
      needs_image = [
          name
          for name, container in build_from_source.items()
          if not flags.FlagIsExplicitlySet(container, 'source')
      ]
      if needs_image:
        raise exceptions.RequiredImageArgumentException(needs_image)
      raise c_exceptions.InvalidArgumentException(
          '--container', 'At most one container can be deployed from source.'
      )

    for name, container in build_from_source.items():
      if not flags.FlagIsExplicitlySet(container, 'source'):
        if console_io.CanPrompt():
          container.source = flags.PromptForDefaultSource(name)
        else:
          if name:
            message = (
                'Container {} requires a container image to deploy (e.g.'
                ' `gcr.io/cloudrun/hello:latest`) if no build source is'
                ' provided.'.format(name)
            )
          else:
            message = (
                'Requires a container image to deploy (e.g.'
                ' `gcr.io/cloudrun/hello:latest`) if no build source is'
                ' provided.'
            )
          raise c_exceptions.RequiredArgumentException(
              '--image',
              message,
          )
    return build_from_source

  def _BuildFromSource(
      self,
      args,
      build_from_source,
      worker_ref,
      already_activated_services,
  ):
    # Only one container can deployed from source
    container = next(iter(build_from_source.values()))
    pack = None
    repo_to_create = None
    source = container.source
    ar_repo = docker_util.DockerRepo(
        project_id=properties.VALUES.core.project.Get(required=True),
        location_id=artifact_registry.RepoRegion(
            args,
        ),
        repo_id='cloud-run-source-deploy',
    )
    if artifact_registry.ShouldCreateRepository(
        ar_repo, skip_activation_prompt=already_activated_services
    ):
      repo_to_create = ar_repo
    # The image is built with latest tag. After build, the image digest
    # from the build result will be added to the image of the worker spec.
    container.image = '{repo}/{worker}'.format(
        repo=ar_repo.GetDockerString(), worker=worker_ref.servicesId
    )
    # Use GCP Buildpacks if Dockerfile doesn't exist
    docker_file = source + '/Dockerfile'
    if os.path.exists(docker_file):
      build_type = BuildType.DOCKERFILE
    else:
      pack = _CreateBuildPack(container)
      build_type = BuildType.BUILDPACKS
    image = None if pack else container.image
    if flags.FlagIsExplicitlySet(args, 'delegate_builds'):
      image = pack[0].get('image') if pack else image
    operation_message = (
        'Building using {build_type} and deploying container to'
    ).format(build_type=build_type.value)
    pretty_print.Info(
        messages_util.GetBuildEquivalentForSourceRunMessage(
            worker_ref.servicesId, pack, source, subgroup='workers '
        )
    )
    return image, pack, source, operation_message, repo_to_create

  def _GetTracker(
      self,
      args,
      worker,
      build_from_source,
      repo_to_create,
  ):
    deployment_stages = stages.WorkerStages(
        include_build=bool(build_from_source),
        include_create_repo=repo_to_create is not None,
    )
    if build_from_source:
      header = 'Building and deploying'
    else:
      header = 'Deploying'
    if worker is None:
      header += ' new worker'
    header += '...'
    return progress_tracker.StagedProgressTracker(
        header,
        deployment_stages,
        failure_message='Deployment failed',
        suppress_output=args.async_,
    )

  def _GetBaseChanges(self, args):
    """Returns the worker config changes with some default settings."""
    changes = flags.GetWorkerConfigurationChanges(args, self.ReleaseTrack())
    changes.insert(
        0,
        config_changes.DeleteAnnotationChange(
            k8s_object.BINAUTHZ_BREAKGLASS_ANNOTATION
        ),
    )
    changes.append(
        config_changes.SetLaunchStageAnnotationChange(self.ReleaseTrack())
    )
    return changes

  def Run(self, args):
    """Deploy a Worker container to Cloud Run."""
    containers = self._ValidateAndGetContainers(args)
    build_from_source = self._ValidateAndGetBuildFromSource(containers)
    worker_ref = args.CONCEPTS.worker.Parse()

    flags.ValidateResource(worker_ref)

    required_apis = [api_enabler.get_run_api()]
    # gcloud-disable-gdu-domain
    if build_from_source:
      required_apis.append('artifactregistry.googleapis.com')
      required_apis.append('cloudbuild.googleapis.com')

    already_activated_services = api_enabler.check_and_enable_apis(
        properties.VALUES.core.project.Get(), required_apis
    )
    # Obtaining the connection context prompts the user to select a region if
    # one hasn't been provided. We want to do this prior to preparing a source
    # deploy so that we can use that region for the Artifact Registry repo.
    conn_context = connection_context.GetConnectionContext(
        args, flags.Product.RUN, self.ReleaseTrack()
    )

    image = None
    pack = None
    source = None
    operation_message = 'Deploying container to'
    repo_to_create = None
    # Build an image from source if source specified
    if build_from_source:
      image, pack, source, operation_message, repo_to_create = (
          self._BuildFromSource(
              args,
              build_from_source,
              worker_ref,
              already_activated_services,
          )
      )

    # Deploy a container with an image
    changes = self._GetBaseChanges(args)

    with serverless_operations.Connect(
        conn_context, already_activated_services
    ) as operations:
      worker = operations.GetWorker(worker_ref)
      pretty_print.Info(
          messages_util.GetStartDeployMessage(
              conn_context,
              worker_ref,
              operation_message,
              resource_kind_lower='worker',
          )
      )
      with self._GetTracker(
          args, worker, build_from_source, repo_to_create
      ) as tracker:
        worker = operations.ReleaseWorker(
            worker_ref,
            changes,
            self.ReleaseTrack(),
            tracker,
            asyn=args.async_,
            prefetch=worker,
            build_image=image,
            build_pack=pack,
            build_source=source,
            repo_to_create=repo_to_create,
            already_activated_services=already_activated_services,
            generate_name=flags.FlagIsExplicitlySet(args, 'revision_suffix'),
        )

      if args.async_:
        pretty_print.Success(
            'Worker [{{bold}}{serv}{{reset}}] is deploying '
            'asynchronously.'.format(serv=worker.name)
        )
      else:
        pretty_print.Success(
            messages_util.GetSuccessMessageForWorkerDeploy(worker)
        )
      return worker


def _CreateBuildPack(container):
  """A helper method to cofigure buildpack."""
  pack = [{'image': container.image}]
  command_arg = getattr(container, 'command', None)
  if command_arg is not None:
    command = ' '.join(command_arg)
    pack[0].update(
        {'envs': ['GOOGLE_ENTRYPOINT="{command}"'.format(command=command)]}
    )
  return pack
