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
"""Utility for parsing Artifact Registry versions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import json

from apitools.base.protorpclite import protojson
from googlecloudsdk.command_lib.artifacts import containeranalysis_util as ca_util
from googlecloudsdk.core import resources


def ShortenRelatedTags(response, unused_args):
  """Convert the tag resources into tag IDs."""
  tags = []
  for t in response.relatedTags:
    tag = resources.REGISTRY.ParseRelativeName(
        t.name,
        'artifactregistry.projects.locations.repositories.packages.tags')
    tags.append(tag.tagsId)

  json_obj = json.loads(protojson.encode_message(response))
  json_obj.pop('relatedTags', None)
  if tags:
    json_obj['relatedTags'] = tags
  # Restore the display format of `metadata` after json conversion.
  if response.metadata is not None:
    json_obj['metadata'] = {
        prop.key: prop.value.string_value
        for prop in response.metadata.additionalProperties
    }
  return json_obj


def ListOccurrences(response, args):
  """Call CA APIs for vulnerabilities if --show-package-vulnerability is set."""
  if not args.show_package_vulnerability:
    return response

  # TODO(b/246801021) Assume all versions are mavenArtifacts until versions API
  # is aware of the package type.
  project, maven_resource = _GenerateMavenResourceFromResponse(response)

  metadata = ca_util.GetMavenArtifactOccurrences(project, maven_resource)

  if metadata.ArtifactsDescribeView():
    response.update(metadata.ArtifactsDescribeView())
  else:
    response.update(
        {'package_vulnerability_summary': 'No vulnerability data found.'})

  return response


def _GenerateMavenResourceFromResponse(response):
  """Convert Versions Describe Response to maven artifact resource name."""
  r = resources.REGISTRY.ParseRelativeName(
      response['name'],
      'artifactregistry.projects.locations.repositories.packages.versions'
  )

  # mavenArtifacts is only present in the v1 API, not the default v1beta2 API
  registry = resources.REGISTRY.Clone()
  registry.RegisterApiByName('artifactregistry', 'v1')

  maven_artifacts_id = r.packagesId + ':' + r.versionsId

  maven_resource = resources.Resource.RelativeName(
      registry.Create(
          'artifactregistry.projects.locations.repositories.mavenArtifacts',
          projectsId=r.projectsId,
          locationsId=r.locationsId,
          repositoriesId=r.repositoriesId,
          mavenArtifactsId=maven_artifacts_id,
      )
  )

  return r.projectsId, maven_resource
