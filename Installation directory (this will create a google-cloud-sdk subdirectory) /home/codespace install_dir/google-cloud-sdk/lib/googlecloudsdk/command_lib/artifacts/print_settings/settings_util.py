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
"""Utility for forming settings for Artifacts Registry repositories."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import base64
import json

from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.api_lib.auth import service_account
from googlecloudsdk.command_lib.artifacts import requests as ar_requests
from googlecloudsdk.command_lib.artifacts import util as ar_util
from googlecloudsdk.command_lib.artifacts.print_settings import apt
from googlecloudsdk.command_lib.artifacts.print_settings import gradle
from googlecloudsdk.command_lib.artifacts.print_settings import mvn
from googlecloudsdk.command_lib.artifacts.print_settings import npm
from googlecloudsdk.command_lib.artifacts.print_settings import python
from googlecloudsdk.command_lib.artifacts.print_settings import yum
from googlecloudsdk.core import config
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io
from googlecloudsdk.core.credentials import creds
from googlecloudsdk.core.credentials import exceptions as creds_exceptions
from googlecloudsdk.core.credentials import store
from googlecloudsdk.core.util import encoding
from googlecloudsdk.core.util import files

_EXT_VERSION = "2.2.0"

_PROJECT_NOT_FOUND_ERROR = """\
Failed to find attribute [project]. \
The attribute can be set in the following ways:
- provide the argument [--project] on the command line
- set the property [core/project]"""

_REPO_NOT_FOUND_ERROR = """\
Failed to find attribute [repository]. \
The attribute can be set in the following ways:
- provide the argument [--repository] on the command line
- set the property [artifacts/repository]"""

_LOCATION_NOT_FOUND_ERROR = """\
Failed to find attribute [location]. \
The attribute can be set in the following ways:
- provide the argument [--location] on the command line
- set the property [artifacts/location]"""


def _GetRequiredProjectValue(args):
  if not args.project and not properties.VALUES.core.project.Get():
    raise ar_exceptions.InvalidInputValueError(_PROJECT_NOT_FOUND_ERROR)
  return ar_util.GetProject(args)


def _GetRequiredRepoValue(args):
  if not args.repository and not properties.VALUES.artifacts.repository.Get():
    raise ar_exceptions.InvalidInputValueError(_REPO_NOT_FOUND_ERROR)
  return ar_util.GetRepo(args)


def _GetRequiredLocationValue(args):
  if not args.location and not properties.VALUES.artifacts.location.Get():
    raise ar_exceptions.InvalidInputValueError(_LOCATION_NOT_FOUND_ERROR)
  return ar_util.GetLocation(args)


def _GetLocationAndRepoPath(args, repo_format):
  """Get resource values and validate user input."""
  repo = _GetRequiredRepoValue(args)
  project = _GetRequiredProjectValue(args)
  location = _GetRequiredLocationValue(args)
  repo_path = project + "/" + repo
  repo = ar_requests.GetRepository(
      "projects/{}/locations/{}/repositories/{}".format(project, location,
                                                        repo))
  if repo.format != repo_format:
    raise ar_exceptions.InvalidInputValueError(
        "Invalid repository type {}. Valid type is {}.".format(
            repo.format, repo_format))
  return location, repo_path


def _GetLocationRepoPathAndMavenConfig(args, repo_format):
  """Get resource values and validate user input."""
  repo = _GetRequiredRepoValue(args)
  project = _GetRequiredProjectValue(args)
  location = _GetRequiredLocationValue(args)
  repo_path = project + "/" + repo
  repo = ar_requests.GetRepository(
      "projects/{}/locations/{}/repositories/{}".format(project, location,
                                                        repo))
  if repo.format != repo_format:
    raise ar_exceptions.InvalidInputValueError(
        "Invalid repository type {}. Valid type is {}.".format(
            repo.format, repo_format))
  return location, repo_path, repo.mavenConfig


def _LoadJsonFile(filename):
  """Checks and validates if given filename is a proper JSON file.

  Args:
    filename: str, path to JSON file.

  Returns:
    bytes, the content of the file.
  """
  content = console_io.ReadFromFileOrStdin(filename, binary=True)
  try:
    json.loads(encoding.Decode(content))
    return content
  except ValueError as e:
    if filename.endswith(".json"):
      raise service_account.BadCredentialFileException(
          "Could not read JSON file {0}: {1}".format(filename, e))
  raise service_account.BadCredentialFileException(
      "Unsupported credential file: {0}".format(filename))


def _GetServiceAccountCreds(args):
  """Gets service account credentials from given file path or default if any.

  Args:
    args: Command arguments.

  Returns:
    str, service account credentials.
  """
  if args.json_key:
    file_content = _LoadJsonFile(args.json_key)
    return base64.b64encode(file_content).decode("utf-8")

  account = properties.VALUES.core.account.Get()
  if not account:
    raise creds_exceptions.NoActiveAccountException()
  cred = store.Load(account, prevent_refresh=True, use_google_auth=True)
  if not cred:
    raise store.NoCredentialsForAccountException(account)

  if _IsServiceAccountCredentials(cred):
    paths = config.Paths()
    json_content = files.ReadFileContents(
        paths.LegacyCredentialsAdcPath(account))
    return base64.b64encode(json_content.encode("utf-8")).decode("utf-8")
  return ""


def _IsServiceAccountCredentials(cred):
  if creds.IsOauth2ClientCredentials(cred):
    return creds.CredentialType.FromCredentials(
        cred) == creds.CredentialType.SERVICE_ACCOUNT
  else:
    return creds.CredentialTypeGoogleAuth.FromCredentials(
        cred) == creds.CredentialTypeGoogleAuth.SERVICE_ACCOUNT


def IsPublicRepo(project, location, repo):
  """Determine if a repository is public.

  Args:
    project: Project name.
    location: Repository location.
    repo: Repository name.

  Returns:
    bool, True if repository is public.
  """
  iam_policy = ar_requests.GetIamPolicy(
      "projects/{}/locations/{}/repositories/{}".format(
          project, location, repo))

  if hasattr(iam_policy, "bindings"):
    for binding in iam_policy.bindings:
      if ("allUsers" in binding.members
          and "artifactregistry.reader" in binding.role):
        return True

  return False


def GetAptSettingsSnippet(args):
  """Forms an apt settings snippet to add to the sources.list.d directory.

  Args:
    args: an argparse namespace. All the arguments that were provided to this
      command invocation.

  Returns:
    An apt settings snippet.
  """
  messages = ar_requests.GetMessages()
  location, repo_path = _GetLocationAndRepoPath(
      args, messages.Repository.FormatValueValuesEnum.APT)
  repo = _GetRequiredRepoValue(args)
  project = _GetRequiredProjectValue(args)

  data = {
      "location": location,
      "project": project,
      "repo": repo,
      "repo_path": repo_path
  }

  if IsPublicRepo(project, location, repo):
    apt_setting_template = apt.PUBLIC_TEMPLATE
  else:
    apt_setting_template = apt.DEFAULT_TEMPLATE
  return apt_setting_template.format(**data)


def GetYumSettingsSnippet(args):
  """Forms a Yum settings snippet to add to the yum.repos.d directory.

  Args:
    args: an argparse namespace. All the arguments that were provided to this
      command invocation.

  Returns:
    A yum settings snippet.
  """
  messages = ar_requests.GetMessages()
  location, repo_path = _GetLocationAndRepoPath(
      args, messages.Repository.FormatValueValuesEnum.YUM)
  repo = _GetRequiredRepoValue(args)
  project = _GetRequiredProjectValue(args)

  data = {"location": location, "repo": repo, "repo_path": repo_path}

  if IsPublicRepo(project, location, repo):
    yum_setting_template = yum.PUBLIC_TEMPLATE
  else:
    yum_setting_template = yum.DEFAULT_TEMPLATE

  return yum_setting_template.format(**data)


def GetNpmSettingsSnippet(args):
  """Forms an npm settings snippet to add to the .npmrc file.

  Args:
    args: an argparse namespace. All the arguments that were provided to this
      command invocation.

  Returns:
    An npm settings snippet.
  """
  messages = ar_requests.GetMessages()
  location, repo_path = _GetLocationAndRepoPath(
      args, messages.Repository.FormatValueValuesEnum.NPM)
  registry_path = "{location}-npm.pkg.dev/{repo_path}/".format(**{
      "location": location,
      "repo_path": repo_path
  })
  configured_registry = "registry"
  if args.scope:
    if not args.scope.startswith("@") or len(args.scope) <= 1:
      raise ar_exceptions.InvalidInputValueError(
          "Scope name must start with \"@\" and be longer than 1 character.")
    configured_registry = args.scope + ":" + configured_registry

  data = {
      "configured_registry": configured_registry,
      "registry_path": registry_path,
      "repo_path": repo_path
  }

  sa_creds = _GetServiceAccountCreds(args)
  if sa_creds:
    npm_setting_template = npm.SERVICE_ACCOUNT_TEMPLATE
    data["password"] = base64.b64encode(
        sa_creds.encode("utf-8")).decode("utf-8")
  else:
    npm_setting_template = npm.NO_SERVICE_ACCOUNT_TEMPLATE
  return npm_setting_template.format(**data)


def GetMavenSnippet(args):
  """Forms a maven snippet to add to the pom.xml file.

  Args:
    args: an argparse namespace. All the arguments that were provided to this
      command invocation.

  Returns:
    str, a maven snippet to add to the pom.xml file.
  """
  messages = ar_requests.GetMessages()
  location, repo_path, maven_cfg = _GetLocationRepoPathAndMavenConfig(
      args, messages.Repository.FormatValueValuesEnum.MAVEN)
  data = {
      "scheme": "artifactregistry",
      "location": location,
      "server_id": "artifact-registry",
      "repo_path": repo_path,
  }
  sa_creds = _GetServiceAccountCreds(args)
  mvn_template = GetMavenTemplate(messages, maven_cfg, sa_creds)

  if sa_creds:
    data["scheme"] = "https"
    data["username"] = "_json_key_base64"
    data["password"] = sa_creds
  else:
    data["extension_version"] = _EXT_VERSION

  return mvn_template.format(**data)


def GetMavenTemplate(messages, maven_cfg, sa_creds):
  """Forms a maven snippet to add to the pom.xml file.

  Args:
    messages: Module, the messages module for the API.
    maven_cfg: MavenRepositoryConfig, the maven configuration proto that
      contains the version policy.
    sa_creds: str, service account credentials.

  Returns:
    str, a maven template to add to pom.xml.
  """
  mvn_template = mvn.NO_SERVICE_ACCOUNT_TEMPLATE
  if maven_cfg and maven_cfg.versionPolicy == messages.MavenRepositoryConfig.VersionPolicyValueValuesEnum.SNAPSHOT:
    mvn_template = mvn.NO_SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE
    if sa_creds:
      mvn_template = mvn.SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE
  elif maven_cfg and maven_cfg.versionPolicy == messages.MavenRepositoryConfig.VersionPolicyValueValuesEnum.RELEASE:
    mvn_template = mvn.NO_SERVICE_ACCOUNT_RELEASE_TEMPLATE
    if sa_creds:
      mvn_template = mvn.SERVICE_ACCOUNT_RELEASE_TEMPLATE
  elif sa_creds:
    mvn_template = mvn.SERVICE_ACCOUNT_TEMPLATE

  return mvn_template


def GetGradleSnippet(args):
  """Forms a gradle snippet to add to the build.gradle file.

  Args:
    args: an argparse namespace. All the arguments that were provided to this
      command invocation.

  Returns:
    str, a gradle snippet to add to build.gradle.
  """
  messages = ar_requests.GetMessages()
  location, repo_path, maven_cfg = _GetLocationRepoPathAndMavenConfig(
      args, messages.Repository.FormatValueValuesEnum.MAVEN)
  sa_creds = _GetServiceAccountCreds(args)
  gradle_template = GetGradleTemplate(messages, maven_cfg, sa_creds)
  data = {"location": location, "repo_path": repo_path}

  if sa_creds:
    data["username"] = "_json_key_base64"
    data["password"] = sa_creds

  else:
    data["extension_version"] = _EXT_VERSION
  return gradle_template.format(**data)


def GetGradleTemplate(messages, maven_cfg, sa_creds):
  """Forms a gradle snippet to add to the build.gradle file.

  Args:
    messages: Module, the messages module for the API.
    maven_cfg: MavenRepositoryConfig, the maven configuration proto that
      contains the version policy..
    sa_creds: str, service account credentials.

  Returns:
    str, a gradle template to add to build.gradle.
  """
  gradle_template = gradle.NO_SERVICE_ACCOUNT_TEMPLATE
  if maven_cfg and maven_cfg.versionPolicy == messages.MavenRepositoryConfig.VersionPolicyValueValuesEnum.SNAPSHOT:
    gradle_template = gradle.NO_SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE
    if sa_creds:
      gradle_template = gradle.SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE
  elif maven_cfg and maven_cfg.versionPolicy == messages.MavenRepositoryConfig.VersionPolicyValueValuesEnum.RELEASE:
    gradle_template = gradle.NO_SERVICE_ACCOUNT_RELEASE_TEMPLATE
    if sa_creds:
      gradle_template = gradle.SERVICE_ACCOUNT_RELEASE_TEMPLATE
  elif sa_creds:
    gradle_template = gradle.SERVICE_ACCOUNT_TEMPLATE

  return gradle_template


def GetPythonSettingsSnippet(args):
  """Forms a Python snippet for .pypirc file (twine) and pip.conf file.

  Args:
    args: an argparse namespace. All the arguments that were provided to this
      command invocation.

  Returns:
    A python snippet.
  """
  messages = ar_requests.GetMessages()
  location, repo_path = _GetLocationAndRepoPath(
      args, messages.Repository.FormatValueValuesEnum.PYTHON)
  repo = _GetRequiredRepoValue(args)
  data = {"location": location, "repo_path": repo_path, "repo": repo}

  sa_creds = _GetServiceAccountCreds(args)

  if sa_creds:
    data["password"] = sa_creds
    return python.SERVICE_ACCOUNT_SETTING_TEMPLATE.format(**data)
  else:
    return python.NO_SERVICE_ACCOUNT_SETTING_TEMPLATE.format(**data)
