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
"""File utils for Artifact Registry commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.command_lib.artifacts import requests
from googlecloudsdk.command_lib.artifacts import util
from googlecloudsdk.core import resources


def EscapeFileName(ref):
  """Escapes slashes and pluses from request names."""
  return resources.REGISTRY.Create(
      "artifactregistry.projects.locations.repositories.files",
      projectsId=ref.projectsId,
      locationsId=ref.locationsId,
      repositoriesId=ref.repositoriesId,
      filesId=
      ref.filesId.replace("/", "%2F").replace("+", "%2B").replace("^", "%5E"),
  )


def EscapeFileNameFromIDs(project_id, location_id, repo_id, file_id):
  """Escapes slashes and pluses from request names."""
  return resources.REGISTRY.Create(
      "artifactregistry.projects.locations.repositories.files",
      projectsId=project_id,
      locationsId=location_id,
      repositoriesId=repo_id,
      filesId=
      file_id.replace("/", "%2F").replace("+", "%2B").replace("^", "%5E"),
  )


def ListGenericFiles(args):
  """Lists the Generic Files stored."""
  client = requests.GetClient()
  messages = requests.GetMessages()
  project = util.GetProject(args)
  location = util.GetLocation(args)
  repo = util.GetRepo(args)
  package = args.package
  version = args.version
  version_path = resources.Resource.RelativeName(
      resources.REGISTRY.Create(
          "artifactregistry.projects.locations.repositories.packages.versions",
          projectsId=project,
          locationsId=location,
          repositoriesId=repo,
          packagesId=package,
          versionsId=version))
  arg_filters = 'owner="{}"'.format(version_path)
  repo_path = resources.Resource.RelativeName(
      resources.REGISTRY.Create(
          "artifactregistry.projects.locations.repositories",
          projectsId=project,
          locationsId=location,
          repositoriesId=repo))
  files = requests.ListFiles(client, messages, repo_path, arg_filters)

  return files
