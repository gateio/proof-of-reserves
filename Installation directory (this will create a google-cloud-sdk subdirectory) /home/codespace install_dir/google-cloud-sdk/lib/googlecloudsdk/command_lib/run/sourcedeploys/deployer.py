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
"""Creates an image from Source."""
from apitools.base.py import encoding
from googlecloudsdk.api_lib.cloudbuild import cloudbuild_util
from googlecloudsdk.api_lib.run import run_util
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.builds import submit_util
from googlecloudsdk.command_lib.run import stages
from googlecloudsdk.command_lib.run.sourcedeploys import sources
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources


# TODO(b/313435281): Bundle these "build_" variables into an object
def CreateImage(
    tracker,
    build_image,
    build_source,
    build_pack,
    release_track,
    already_activated_services,
    region: str,
    resource_ref,
    delegate_builds=False,
    base_image=None,
):
  """Creates an image from Source."""
  # Automatic base image updates implies call to build API.
  delegate_builds = base_image or delegate_builds
  # Upload source and call build API if it's in alpha and `--delegate-builds`
  # flag is set. Otherwise, default behavior stays the same.
  if release_track is base.ReleaseTrack.ALPHA and delegate_builds:
    submit_build_request = _PrepareSubmitBuildRequest(
        tracker,
        build_image,
        build_source,
        build_pack,
        region,
        resource_ref,
        release_track,
        base_image,
    )
    response_dict, build_log_url = _SubmitBuild(
        tracker,
        release_track,
        region,
        submit_build_request,
    )
  else:
    build_messages, build_config = _PrepareBuildConfig(
        tracker,
        build_image,
        build_source,
        build_pack,
        release_track,
        region,
        resource_ref,
    )
    response_dict, build_log_url = _BuildFromSource(
        tracker,
        build_messages,
        build_config,
        skip_activation_prompt=already_activated_services,
    )

  if response_dict and response_dict['status'] != 'SUCCESS':
    tracker.FailStage(
        stages.BUILD_READY,
        None,
        message=(
            'Container build failed and '
            'logs are available at [{build_log_url}].'.format(
                build_log_url=build_log_url
            )
        ),
    )
    return None  # Failed to create an image
  else:
    tracker.CompleteStage(stages.BUILD_READY)
    return response_dict['results']['images'][0]['digest']


def _PrepareBuildConfig(
    tracker,
    build_image,
    build_source,
    build_pack,
    release_track,
    region,
    resource_ref,
):
  """Upload the provided build source and prepare build config for cloud build."""
  tracker.StartStage(stages.UPLOAD_SOURCE)
  tracker.UpdateHeaderMessage('Uploading sources.')
  build_messages = cloudbuild_util.GetMessagesModule()

  # Make this the default after CRF is out of Alpha
  if release_track is base.ReleaseTrack.ALPHA:
    source = sources.Upload(build_source, region, resource_ref)

    # add the source uri as a label to the image
    # https://github.com/GoogleCloudPlatform/buildpacks/blob/main/cmd/utils/label/README.md
    uri = f'gs://{source.bucket}/{source.name}#{source.generation}'
    if build_pack is not None:
      envs = build_pack[0].get('envs', [])
      envs.append(f'GOOGLE_LABEL_SOURCE={uri}')  # "google.source"
      build_pack[0].update({'envs': envs})

    # force disable Kaniko since we don't support customizing the build here.
    properties.VALUES.builds.use_kaniko.Set(False)
    build_config = submit_util.CreateBuildConfig(
        build_image,
        no_cache=False,
        messages=build_messages,
        substitutions=None,
        arg_config=None,
        is_specified_source=True,
        no_source=False,
        source=build_source,
        gcs_source_staging_dir=None,
        ignore_file=None,
        arg_gcs_log_dir=None,
        arg_machine_type=None,
        arg_disk_size=None,
        arg_worker_pool=None,
        arg_dir=None,
        arg_revision=None,
        arg_git_source_dir=None,
        arg_git_source_revision=None,
        buildpack=build_pack,
        hide_logs=True,
        skip_set_source=True,
        client_tag='gcloudrun',
    )

    # is docker build
    if build_pack is None:
      assert build_config.steps[0].name == 'gcr.io/cloud-builders/docker'
      # https://docs.docker.com/engine/reference/commandline/image_build/
      build_config.steps[0].args.extend(
          ['--label', f'google.source={uri}']
      )

    build_config.source = build_messages.Source(
        storageSource=build_messages.StorageSource(
            bucket=source.bucket,
            object=source.name,
            generation=source.generation,
        )
    )
  else:
    # force disable Kaniko since we don't support customizing the build here.
    properties.VALUES.builds.use_kaniko.Set(False)
    build_config = submit_util.CreateBuildConfig(
        build_image,
        no_cache=False,
        messages=build_messages,
        substitutions=None,
        arg_config=None,
        is_specified_source=True,
        no_source=False,
        source=build_source,
        gcs_source_staging_dir=None,
        ignore_file=None,
        arg_gcs_log_dir=None,
        arg_machine_type=None,
        arg_disk_size=None,
        arg_worker_pool=None,
        arg_dir=None,
        arg_revision=None,
        arg_git_source_dir=None,
        arg_git_source_revision=None,
        buildpack=build_pack,
        hide_logs=True,
        client_tag='gcloudrun',
    )

  tracker.CompleteStage(stages.UPLOAD_SOURCE)
  return build_messages, build_config


def _BuildFromSource(
    tracker, build_messages, build_config, skip_activation_prompt=False
):
  """Build an image from source if a user specifies a source when deploying."""
  build_region = cloudbuild_util.DEFAULT_REGION
  build, _ = submit_util.Build(
      build_messages,
      True,
      build_config,
      hide_logs=True,
      build_region=build_region,
      skip_activation_prompt=skip_activation_prompt,
  )
  build_op = f'projects/{build.projectId}/locations/{build_region}/operations/{build.id}'
  build_op_ref = resources.REGISTRY.ParseRelativeName(
      build_op, collection='cloudbuild.projects.locations.operations'
  )
  build_log_url = build.logUrl
  tracker.StartStage(stages.BUILD_READY)
  tracker.UpdateHeaderMessage('Building Container.')
  tracker.UpdateStage(
      stages.BUILD_READY,
      'Logs are available at [{build_log_url}].'.format(
          build_log_url=build_log_url
      ),
  )

  response_dict = _PollUntilBuildCompletes(build_op_ref)
  return response_dict, build_log_url


def _PrepareSubmitBuildRequest(
    tracker,
    build_image,
    build_source,
    build_pack,
    region,
    resource_ref,
    release_track,
    base_image,
):
  """Upload the provided build source and prepare submit build request."""
  messages = run_util.GetMessagesModule(release_track)
  tracker.StartStage(stages.UPLOAD_SOURCE)
  tracker.UpdateHeaderMessage('Uploading sources.')
  source = sources.Upload(build_source, region, resource_ref)
  tracker.CompleteStage(stages.UPLOAD_SOURCE)
  parent = 'projects/{project}/locations/{region}'.format(
      project=properties.VALUES.core.project.Get(required=True),
      region=region)
  storage_source = messages.GoogleCloudRunV2StorageSource(
      bucket=source.bucket, object=source.name, generation=source.generation)

  buildpack_build = None
  docker_build = None
  if build_pack:
    function_target = None
    # https://github.com/GoogleCloudPlatform/buildpacks/blob/main/cmd/utils/label/README.md
    # uri = f'gs://{source.bucket}/{source.name}#{source.generation}'
    envs = build_pack[0].get('envs', [])
    function_target_env = [x for x in envs
                           if x.startswith('GOOGLE_FUNCTION_TARGET')]
    if function_target_env:
      function_target = function_target_env[0].split('=')[1]
    buildpack_build = messages.GoogleCloudRunV2BuildpacksBuild(
        baseImage=base_image, functionTarget=function_target)
  else:
    docker_build = messages.GoogleCloudRunV2DockerBuild()
  submit_build_request = messages.RunProjectsLocationsBuildsSubmitRequest(
      parent=parent,
      googleCloudRunV2SubmitBuildRequest=messages.GoogleCloudRunV2SubmitBuildRequest(
          storageSource=storage_source,
          imageUri=build_image,
          buildpackBuild=buildpack_build,
          dockerBuild=docker_build,),
      )
  return submit_build_request


def _SubmitBuild(
    tracker,
    release_track,
    region,
    submit_build_request,
):
  """Calls Build API to submit a build."""
  run_client = run_util.GetClientInstance(release_track)
  build_messages = cloudbuild_util.GetMessagesModule()

  build_response = run_client.projects_locations_builds.Submit(
      submit_build_request)
  build_op = build_response.buildOperation
  json = encoding.MessageToJson(build_op.metadata)
  build = encoding.JsonToMessage(
      build_messages.BuildOperationMetadata, json).build
  name = f'projects/{build.projectId}/locations/{region}/operations/{build.id}'

  build_op_ref = resources.REGISTRY.ParseRelativeName(
      name, collection='cloudbuild.projects.locations.operations'
  )
  build_log_url = build.logUrl
  tracker.StartStage(stages.BUILD_READY)
  tracker.UpdateHeaderMessage('Building Container.')
  tracker.UpdateStage(
      stages.BUILD_READY,
      'Logs are available at [{build_log_url}].'.format(
          build_log_url=build_log_url
      ),
  )
  response_dict = _PollUntilBuildCompletes(build_op_ref)
  return response_dict, build_log_url


def _PollUntilBuildCompletes(build_op_ref):
  client = cloudbuild_util.GetClientInstance()
  poller = waiter.CloudOperationPoller(
      client.projects_builds, client.operations
  )
  operation = waiter.PollUntilDone(poller, build_op_ref)
  return encoding.MessageToPyValue(operation.response)
