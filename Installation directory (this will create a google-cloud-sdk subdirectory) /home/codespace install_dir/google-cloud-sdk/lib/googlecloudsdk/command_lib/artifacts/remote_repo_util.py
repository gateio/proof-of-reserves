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
"""Remote repo utils for Artifact Registry repository commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import requests as ar_requests
from googlecloudsdk.command_lib.util.apis import arg_utils


def Args():
  """Adds the remote-<facade>-repo flags."""
  # We need to do this because these flags need to be able to accept either a
  # PublicRepository enum or a string registry URI.
  return [
      base.Argument(
          "--remote-mvn-repo",
          help=_RemoteRepoHelpText(facade="Maven", hide_custom_remotes=False),
      ),
      base.Argument(
          "--remote-docker-repo",
          help=_RemoteRepoHelpText(facade="Docker", hide_custom_remotes=False),
      ),
      base.Argument(
          "--remote-npm-repo",
          help=_RemoteRepoHelpText(facade="Npm", hide_custom_remotes=False),
      ),
      base.Argument(
          "--remote-python-repo",
          help=_RemoteRepoHelpText(facade="Python", hide_custom_remotes=False),
      ),
      base.Argument(
          "--remote-apt-repo",
          help=_OsPackageRemoteRepoHelpText(
              facade="Apt", hide_custom_remotes=True
          ),
      ),
      base.Argument(
          "--remote-yum-repo",
          help=_OsPackageRemoteRepoHelpText(
              facade="Yum", hide_custom_remotes=True
          ),
      ),
      base.Argument(
          "--remote-username",
          help="Remote Repository upstream registry username.",
      ),
      base.Argument(
          "--remote-password-secret-version",
          help="""\
          Secret Manager secret version that contains password for the
          remote repository upstream.
          """,
      ),
  ]


def IsRemoteRepoRequest(repo_args) -> bool:
  """Returns whether or not the repo mode specifies a remote repository."""
  return (
      hasattr(repo_args, "mode")
      and arg_utils.ChoiceToEnumName(repo_args.mode) == "REMOTE_REPOSITORY"
  )


def AppendRemoteRepoConfigToRequest(messages, repo_args, request):
  """Adds remote repository config to CreateRepositoryRequest or UpdateRepositoryRequest."""
  remote_cfg = messages.RemoteRepositoryConfig()
  remote_cfg.description = repo_args.remote_repo_config_desc
  # Credentials
  username = repo_args.remote_username
  secret = repo_args.remote_password_secret_version
  if username or secret:
    creds = messages.UpstreamCredentials()
    creds.usernamePasswordCredentials = messages.UsernamePasswordCredentials()
    if username:
      creds.usernamePasswordCredentials.username = username
    if secret:
      creds.usernamePasswordCredentials.passwordSecretVersion = secret
    remote_cfg.upstreamCredentials = creds

  # Disable Remote Validation
  if repo_args.disable_remote_validation:
    remote_cfg.disableUpstreamValidation = True

  # MAVEN
  if repo_args.remote_mvn_repo:
    remote_cfg.mavenRepository = messages.MavenRepository()
    facade, remote_input = "Maven", repo_args.remote_mvn_repo
    enum_message = _ChoiceToRemoteEnum(facade, remote_input)
    if enum_message:  # input is PublicRepository
      remote_cfg.mavenRepository.publicRepository = enum_message
    elif _IsRemoteURI(remote_input):  # input is CustomRepository
      remote_cfg.mavenRepository.customRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigMavenRepositoryCustomRepository()
      )
      remote_cfg.mavenRepository.customRepository.uri = remote_input
    elif _IsARRemote(remote_input):  # input is ArtifactRegistryRepository
      remote_cfg.mavenRepository.artifactRegistryRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigMavenRepositoryArtifactRegistryRepository()
      )
      remote_cfg.mavenRepository.artifactRegistryRepository.repository = (
          remote_input
      )
    else:  # raise error
      _RaiseRemoteRepoUpstreamError(facade, remote_input)

  # DOCKER
  elif repo_args.remote_docker_repo:
    remote_cfg.dockerRepository = messages.DockerRepository()
    facade, remote_input = "Docker", repo_args.remote_docker_repo
    enum_message = _ChoiceToRemoteEnum(facade, remote_input)
    if enum_message:  # input is PublicRepository
      remote_cfg.dockerRepository.publicRepository = enum_message
    elif _IsRemoteURI(remote_input):  # input is CustomRepository
      remote_cfg.dockerRepository.customRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigDockerRepositoryCustomRepository()
      )
      remote_cfg.dockerRepository.customRepository.uri = remote_input
    elif _IsARRemote(remote_input):  # input is ArtifactRegistryRepository
      remote_cfg.dockerRepository.artifactRegistryRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigDockerRepositoryArtifactRegistryRepository()
      )
      remote_cfg.dockerRepository.artifactRegistryRepository.repository = (
          remote_input
      )
    else:  # raise error
      _RaiseRemoteRepoUpstreamError(facade, remote_input)

  # NPM
  elif repo_args.remote_npm_repo:
    remote_cfg.npmRepository = messages.NpmRepository()
    facade, remote_input = "Npm", repo_args.remote_npm_repo
    enum_message = _ChoiceToRemoteEnum(facade, remote_input)
    if enum_message:  # input is PublicRepository
      remote_cfg.npmRepository.publicRepository = enum_message
    elif _IsRemoteURI(remote_input):  # input is CustomRepository
      remote_cfg.npmRepository.customRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigNpmRepositoryCustomRepository()
      )
      remote_cfg.npmRepository.customRepository.uri = remote_input
    elif _IsARRemote(remote_input):  # input is ArtifactRegistryRepository
      remote_cfg.npmRepository.artifactRegistryRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigNpmRepositoryArtifactRegistryRepository()
      )
      remote_cfg.npmRepository.artifactRegistryRepository.repository = (
          remote_input
      )
    else:  # raise error
      _RaiseRemoteRepoUpstreamError(facade, remote_input)

  # PYTHON
  elif repo_args.remote_python_repo:
    remote_cfg.pythonRepository = messages.PythonRepository()
    facade, remote_input = "Python", repo_args.remote_python_repo
    enum_message = _ChoiceToRemoteEnum(facade, remote_input)
    if enum_message:  # input is PublicRepository
      remote_cfg.pythonRepository.publicRepository = enum_message
    elif _IsRemoteURI(remote_input):  # input is CustomRepository
      remote_cfg.pythonRepository.customRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigPythonRepositoryCustomRepository()
      )
      remote_cfg.pythonRepository.customRepository.uri = remote_input
    elif _IsARRemote(remote_input):  # input is ArtifactRegistryRepository
      remote_cfg.pythonRepository.artifactRegistryRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigPythonRepositoryArtifactRegistryRepository()
      )
      remote_cfg.pythonRepository.artifactRegistryRepository.repository = (
          remote_input
      )
    else:  # raise error
      _RaiseRemoteRepoUpstreamError(facade, remote_input)

  # APT
  elif repo_args.remote_apt_repo:
    remote_cfg.aptRepository = messages.AptRepository()
    facade, remote_base, remote_path = (
        "Apt",
        repo_args.remote_apt_repo,
        repo_args.remote_apt_repo_path,
    )
    enum_message = _ChoiceToRemoteEnum(facade, remote_base)
    if enum_message:  # input is PublicRepository
      remote_cfg.aptRepository.publicRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigAptRepositoryPublicRepository()
      )
      remote_cfg.aptRepository.publicRepository.repositoryBase = enum_message
      remote_cfg.aptRepository.publicRepository.repositoryPath = remote_path
    elif _IsRemoteURI(_OsPackageUri(remote_base, remote_path)):
      # input is CustomRepository
      remote_cfg.aptRepository.customRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigAptRepositoryCustomRepository()
      )
      remote_cfg.aptRepository.customRepository.uri = _OsPackageUri(
          remote_base, remote_path
      )
    elif _IsARRemote(remote_base):  # input is ArtifactRegistryRepository
      if remote_path:
        raise ar_exceptions.InvalidInputValueError(
            "--remote-apt-repo-path is not supported for Artifact Registry"
            " Repository upstream."
        )
      remote_cfg.aptRepository.artifactRegistryRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigAptRepositoryArtifactRegistryRepository()
      )
      remote_cfg.aptRepository.artifactRegistryRepository.repository = (
          remote_base
      )
    else:  # raise error
      _RaiseRemoteRepoUpstreamError(facade, remote_base)

  # YUM
  elif repo_args.remote_yum_repo:
    remote_cfg.yumRepository = messages.YumRepository()
    facade, remote_base, remote_path = (
        "Yum",
        repo_args.remote_yum_repo,
        repo_args.remote_yum_repo_path,
    )
    enum_message = _ChoiceToRemoteEnum(facade, remote_base)
    if enum_message:  # input is PublicRepository
      remote_cfg.yumRepository.publicRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigYumRepositoryPublicRepository()
      )
      remote_cfg.yumRepository.publicRepository.repositoryBase = enum_message
      remote_cfg.yumRepository.publicRepository.repositoryPath = remote_path
    elif _IsRemoteURI(_OsPackageUri(remote_base, remote_path)):
      # input is CustomRepository
      remote_cfg.yumRepository.customRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigYumRepositoryCustomRepository()
      )
      remote_cfg.yumRepository.customRepository.uri = _OsPackageUri(
          remote_base, remote_path
      )
    elif _IsARRemote(remote_base):  # input is ArtifactRegistryRepository
      if remote_path:
        raise ar_exceptions.InvalidInputValueError(
            "--remote-yum-repo-path is not supported for Artifact Registry"
            " Repository upstream."
        )
      remote_cfg.yumRepository.artifactRegistryRepository = (
          messages.GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigYumRepositoryArtifactRegistryRepository()
      )
      remote_cfg.yumRepository.artifactRegistryRepository.repository = (
          remote_base
      )
    else:  # raise error
      _RaiseRemoteRepoUpstreamError(facade, remote_base)

  else:
    return request

  request.repository.remoteRepositoryConfig = remote_cfg
  return request


def _RemoteRepoHelpText(facade: str, hide_custom_remotes: bool) -> str:
  if hide_custom_remotes:
    return """\
({facade} only) Repo upstream for {facade_lower} remote repository.
REMOTE_{command}_REPO must be one of: [{enums}].
""".format(
        facade=facade,
        facade_lower=facade.lower(),
        command=_LanguagePackageCommandName(facade),
        enums=_EnumsStrForFacade(facade),
    )
  return """\
({facade} only) Repo upstream for {facade_lower} remote repository.
REMOTE_{command}_REPO can be either:
  - one of the following enums: [{enums}].
  - an http/https custom registry uri (ex: https://my.{facade_lower}.registry)
""".format(
      facade=facade,
      facade_lower=facade.lower(),
      command=_LanguagePackageCommandName(facade),
      enums=_EnumsStrForFacade(facade),
  )


def _OsPackageRemoteRepoHelpText(facade: str, hide_custom_remotes: bool) -> str:
  if hide_custom_remotes:
    return """\
({facade} only) Repository base for {facade_lower} remote repository.
REMOTE_{facade_upper}_REPO must be one of: [{enums}].
""".format(
        facade=facade,
        facade_lower=facade.lower(),
        facade_upper=facade.upper(),
        enums=_EnumsStrForFacade(facade),
    )
  return """\
({facade} only) Repository base for {facade_lower} remote repository.
REMOTE_{facade_upper}_REPO can be either:
  - one of the following enums: [{enums}].
  - an http/https custom registry uri (ex: https://my.{facade_lower}.registry)
""".format(
      facade=facade,
      facade_lower=facade.lower(),
      facade_upper=facade.upper(),
      enums=_EnumsStrForFacade(facade),
  )


def _LanguagePackageCommandName(facade: str) -> str:
  if facade == "Maven":
    return "MVN"
  return facade.upper()


def _ChoiceToRemoteEnum(facade: str, remote_input: str):
  """Converts the remote repo input to a PublicRepository Enum message or None."""
  enums = _EnumsMessageForFacade(facade)
  name = arg_utils.ChoiceToEnumName(remote_input)
  try:
    return enums.lookup_by_name(name)
  except KeyError:
    return None


def _EnumsMessageForFacade(facade: str):
  """Returns the PublicRepository enum messages for a facade."""
  facade_to_enum = {
      "Maven": (
          ar_requests.GetMessages()
          .MavenRepository()
          .PublicRepositoryValueValuesEnum
      ),
      "Docker": (
          ar_requests.GetMessages()
          .DockerRepository()
          .PublicRepositoryValueValuesEnum
      ),
      "Npm": (
          ar_requests.GetMessages()
          .NpmRepository()
          .PublicRepositoryValueValuesEnum
      ),
      "Python": (
          ar_requests.GetMessages()
          .PythonRepository()
          .PublicRepositoryValueValuesEnum
      ),
      "Apt": (
          ar_requests.GetMessages()
          .GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigAptRepositoryPublicRepository()
          .RepositoryBaseValueValuesEnum
      ),
      "Yum": (
          ar_requests.GetMessages()
          .GoogleDevtoolsArtifactregistryV1RemoteRepositoryConfigYumRepositoryPublicRepository()
          .RepositoryBaseValueValuesEnum
      ),
  }
  return facade_to_enum[facade]


def _EnumsStrForFacade(facade: str) -> str:
  """Returns the human-readable PublicRepository enum strings for a facade."""
  return _EnumsMessageToStr(_EnumsMessageForFacade(facade))


def _EnumsMessageToStr(enums) -> str:
  """Returns the human-readable PublicRepository enum strings."""
  return ", ".join(
      arg_utils.EnumNameToChoice(name)
      for name, number in sorted(enums.to_dict().items())
      if number != 0  # Ignore UNSPECIFIED enum values.
  )


def _OsPackageUri(remote_base, remote_path):
  # Don't concatenate if remote_path not given.
  if not remote_path:
    return remote_base
  # Add '/' to end of remote_base if not already present.
  if remote_base[-1] != "/":
    remote_base = remote_base + "/"
  return remote_base + remote_path


def _IsRemoteURI(remote_input: str) -> bool:
  return remote_input.startswith("https://") or remote_input.startswith(
      "http://"
  )


def _IsARRemote(remote_input: str) -> bool:
  return remote_input.startswith("projects/")


def _RaiseRemoteRepoUpstreamError(facade: str, remote_input: str):
  raise ar_exceptions.InvalidInputValueError("""\
Invalid repo upstream for remote repository: '{remote_input}'. Valid choices are: [{enums}].
If you intended to enter a custom upstream URI, this value must start with 'https://' or 'http://'.
""".format(remote_input=remote_input, enums=_EnumsStrForFacade(facade)))
