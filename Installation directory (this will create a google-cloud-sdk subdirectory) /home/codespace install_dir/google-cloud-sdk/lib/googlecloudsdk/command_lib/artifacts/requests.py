# -*- coding: utf-8 -*- #
# Copyright 2020 Google LLC. All Rights Reserved.
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
"""Utility for making API calls."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager
from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.api_lib.cloudkms import iam as kms_iam
from googlecloudsdk.api_lib.cloudresourcemanager import projects_api
from googlecloudsdk.api_lib.iam import util as iam_api
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.command_lib.iam import iam_util
from googlecloudsdk.command_lib.projects import util as project_util
from googlecloudsdk.core import resources

ARTIFACTREGISTRY_API_NAME = "artifactregistry"
ARTIFACTREGISTRY_API_VERSION = "v1"

STORAGE_API_NAME = "storage"
STORAGE_API_VERSION = "v1"

_GCR_PERMISSION = "storage.objects.list"

CRYPTO_KEY_COLLECTION = "cloudkms.projects.locations.keyRings.cryptoKeys"

REDIRECT_PERMISSIONS = ["storage.buckets.update"]


def GetStorageClient():
  return apis.GetClientInstance(STORAGE_API_NAME, STORAGE_API_VERSION)


def GetStorageMessages():
  return apis.GetMessagesModule(STORAGE_API_NAME, STORAGE_API_VERSION)


def GetClient(skip_activation_prompt=False):
  return apis.GetClientInstance(
      ARTIFACTREGISTRY_API_NAME,
      ARTIFACTREGISTRY_API_VERSION,
      skip_activation_prompt=skip_activation_prompt,
  )


def GetMessages():
  return apis.GetMessagesModule(ARTIFACTREGISTRY_API_NAME,
                                ARTIFACTREGISTRY_API_VERSION)


def GetClientV1beta2():
  return apis.GetClientInstance(ARTIFACTREGISTRY_API_NAME,
                                "v1beta2")


def GetMessagesV1beta2():
  return apis.GetMessagesModule(ARTIFACTREGISTRY_API_NAME,
                                "v1beta2")


def DeleteTag(client, messages, tag):
  """Deletes a tag by its name."""
  delete_tag_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesTagsDeleteRequest(
      name=tag)
  err = client.projects_locations_repositories_packages_tags.Delete(
      delete_tag_req)
  if not isinstance(err, messages.Empty):
    raise ar_exceptions.ArtifactRegistryError(
        "Failed to delete tag {}: {}".format(tag, err))


def CreateDockerTag(client, messages, docker_tag, docker_version):
  """Creates a tag associated with the given docker version."""
  tag = messages.Tag(
      name=docker_tag.GetTagName(), version=docker_version.GetVersionName())
  create_tag_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesTagsCreateRequest(
      parent=docker_tag.GetPackageName(), tag=tag, tagId=docker_tag.tag)
  return client.projects_locations_repositories_packages_tags.Create(
      create_tag_req)


def GetTag(client, messages, tag):
  """Gets a tag by its name."""
  get_tag_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesTagsGetRequest(
      name=tag)
  return client.projects_locations_repositories_packages_tags.Get(get_tag_req)


def DeleteVersion(client, messages, version):
  """Deletes a version by its name."""
  delete_ver_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesVersionsDeleteRequest(
      name=version)
  return client.projects_locations_repositories_packages_versions.Delete(
      delete_ver_req)


def DeletePackage(client, messages, package):
  """Deletes a package by its name."""
  delete_pkg_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesDeleteRequest(
      name=package)
  return client.projects_locations_repositories_packages.Delete(delete_pkg_req)


def GetVersion(client, messages, version):
  """Gets a version by its name."""
  client = GetClient()
  messages = GetMessages()
  get_ver_req = (
      messages
      .ArtifactregistryProjectsLocationsRepositoriesPackagesTagsGetRequest(
          name=version))
  return client.projects_locations_repositories_packages_tags.Get(get_ver_req)


def GetVersionFromTag(client, messages, tag):
  """Gets a version name by a tag name."""
  get_tag_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesTagsGetRequest(
      name=tag)
  get_tag_res = client.projects_locations_repositories_packages_tags.Get(
      get_tag_req)
  if not get_tag_res.version or len(get_tag_res.version.split("/")) != 10:
    raise ar_exceptions.ArtifactRegistryError(
        "Internal error. Corrupted tag: {}".format(tag))
  return get_tag_res.version.split("/")[-1]


def ListTags(client, messages, package, page_size=None):
  """Lists all tags under a package with the given package name."""
  list_tags_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesTagsListRequest(
      parent=package)
  return list(
      list_pager.YieldFromList(
          client.projects_locations_repositories_packages_tags,
          list_tags_req,
          batch_size=page_size,
          batch_size_attribute="pageSize",
          field="tags"))


def ListVersionTags(client, messages, package, version, page_size=None):
  """Lists tags associated with the given version."""
  list_tags_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesTagsListRequest(
      parent=package, filter="version=\"{}\"".format(version))
  return list(
      list_pager.YieldFromList(
          client.projects_locations_repositories_packages_tags,
          list_tags_req,
          batch_size=page_size,
          batch_size_attribute="pageSize",
          field="tags"))


def ListPackages(client, messages, repo, page_size=None):
  """Lists all packages under a repository."""
  list_pkgs_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesListRequest(
      parent=repo)
  return list(
      list_pager.YieldFromList(
          client.projects_locations_repositories_packages,
          list_pkgs_req,
          batch_size=page_size,
          batch_size_attribute="pageSize",
          field="packages"))


def ListVersions(client, messages, pkg, version_view,
                 page_size=None, order_by=None, limit=None):
  """Lists all versions under a package."""
  page_limit = limit
  if limit is None or (page_size is not None and page_size < limit):
    page_limit = page_size

  list_vers_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesVersionsListRequest(
      parent=pkg, view=version_view, orderBy=order_by)
  return list(
      list_pager.YieldFromList(
          client.projects_locations_repositories_packages_versions,
          list_vers_req,
          limit=limit,
          batch_size=page_limit,
          batch_size_attribute="pageSize",
          field="versions"))


def ListRepositories(project, page_size=None):
  """Lists all repositories under a project."""
  client = GetClient()
  messages = GetMessages()
  list_repos_req = messages.ArtifactregistryProjectsLocationsRepositoriesListRequest(
      parent=project)
  return list(
      list_pager.YieldFromList(
          client.projects_locations_repositories,
          list_repos_req,
          batch_size=page_size,
          batch_size_attribute="pageSize",
          field="repositories"))


def ListFiles(client, messages, repo, arg_filters, page_size=None):
  """Lists all files under a repository."""
  client = GetClient()
  messages = GetMessages()
  list_files_req = (
      messages.ArtifactregistryProjectsLocationsRepositoriesFilesListRequest(
          parent=repo, filter=arg_filters))
  return list(
      list_pager.YieldFromList(
          client.projects_locations_repositories_files,
          list_files_req,
          batch_size=page_size,
          batch_size_attribute="pageSize",
          field="files"))


def GetRepository(repo, skip_activation_prompt=False):
  """Gets the repository given its name."""
  client = GetClient(skip_activation_prompt)
  messages = GetMessages()
  get_repo_req = messages.ArtifactregistryProjectsLocationsRepositoriesGetRequest(
      name=repo)
  get_repo_res = client.projects_locations_repositories.Get(get_repo_req)
  return get_repo_res


def GetIamPolicy(repo_res):
  """Gets the IAM policy for the specified repository."""
  client = GetClient()
  messages = GetMessages()
  get_iam_policy_req = messages.ArtifactregistryProjectsLocationsRepositoriesGetIamPolicyRequest(
      resource=repo_res)
  get_iam_policy_res = client.projects_locations_repositories.GetIamPolicy(
      get_iam_policy_req)
  return get_iam_policy_res


def SetIamPolicy(repo_res, policy):
  """Sets the IAM policy for the specified repository."""
  client = GetClient()

  ar_messages = GetMessages()

  # pylint: disable=line-too-long
  set_iam_policy_req = ar_messages.ArtifactregistryProjectsLocationsRepositoriesSetIamPolicyRequest(
      resource=repo_res,
      setIamPolicyRequest=ar_messages.SetIamPolicyRequest(policy=policy),
  )
  return client.projects_locations_repositories.SetIamPolicy(set_iam_policy_req)


def CreateRepository(
    project, location, repository, skip_activation_prompt=False
):
  """Creates the repository given its parent.

  Args:
    project: str: The project to create the repository in.
    location: str: The region to create the repository in.
    repository: messages.Repository to create.
    skip_activation_prompt: bool: If true, do not prompt for service activation

  Returns:
    The resulting operation from the create request.
  """
  client = GetClient(skip_activation_prompt)
  messages = GetMessages()
  request = messages.ArtifactregistryProjectsLocationsRepositoriesCreateRequest(
      parent="projects/{}/locations/{}".format(project, location),
      repositoryId=repository.name.split("/")[-1],
      repository=repository)
  return client.projects_locations_repositories.Create(request)


def GetPackage(package):
  """Gets the package given its name."""
  client = GetClient()
  messages = GetMessages()
  get_package_req = messages.ArtifactregistryProjectsLocationsRepositoriesPackagesGetRequest(
      name=package)
  get_package_res = client.projects_locations_repositories_packages.Get(
      get_package_req)
  return get_package_res


def ListLocations(project_id, page_size=None):
  """Lists all locations for a given project."""
  client = GetClientV1beta2()
  messages = GetMessagesV1beta2()
  list_locs_req = messages.ArtifactregistryProjectsLocationsListRequest(
      name="projects/" + project_id)
  locations = list_pager.YieldFromList(
      client.projects_locations,
      list_locs_req,
      batch_size=page_size,
      batch_size_attribute="pageSize",
      field="locations")
  return sorted([loc.locationId for loc in locations])


def TestStorageIAMPermission(bucket, project):
  """Tests storage IAM permission for a given bucket for the user project."""
  client = GetStorageClient()
  messages = GetStorageMessages()
  test_req = messages.StorageBucketsTestIamPermissionsRequest(
      bucket=bucket, permissions=_GCR_PERMISSION, userProject=project)
  return client.buckets.TestIamPermissions(test_req)


def GetCryptoKeyPolicy(kms_key):
  """Gets the IAM policy for a given crypto key."""
  crypto_key_ref = resources.REGISTRY.ParseRelativeName(
      relative_name=kms_key, collection=CRYPTO_KEY_COLLECTION)
  return kms_iam.GetCryptoKeyIamPolicy(crypto_key_ref)


def AddCryptoKeyPermission(kms_key, service_account):
  """Adds Encrypter/Decrypter role to the given service account."""
  crypto_key_ref = resources.REGISTRY.ParseRelativeName(
      relative_name=kms_key, collection=CRYPTO_KEY_COLLECTION)
  return kms_iam.AddPolicyBindingToCryptoKey(
      crypto_key_ref, service_account,
      "roles/cloudkms.cryptoKeyEncrypterDecrypter")


def GetServiceAccount(service_account):
  """Gets the service account given its email."""
  client, messages = iam_api.GetClientAndMessages()
  return client.projects_serviceAccounts.Get(
      messages.IamProjectsServiceAccountsGetRequest(
          name=iam_util.EmailToAccountResourceName(service_account)))


def TestRedirectionIAMPermission(project):
  """Tests the user has the storage.buckets.update IAM permission on the project."""
  project_ref = project_util.ParseProject(project)
  result = projects_api.TestIamPermissions(project_ref, REDIRECT_PERMISSIONS)
  return set(REDIRECT_PERMISSIONS) == set(result.permissions)


def GetProjectSettings(project_id):
  client = GetClient()
  messages = GetMessages()
  get_settings_req = messages.ArtifactregistryProjectsGetProjectSettingsRequest(
      name="projects/" + project_id + "/projectSettings")
  return client.projects.GetProjectSettings(get_settings_req)


def GetVPCSCConfig(project_id, location_id):
  """Gets VPC SC Config on the project and location."""
  client = GetClient()
  messages = GetMessages()
  get_vpcsc_req = messages.ArtifactregistryProjectsLocationsGetVpcscConfigRequest(
      name="projects/" + project_id + "/locations/" + location_id +
      "/vpcscConfig")
  return client.projects_locations.GetVpcscConfig(get_vpcsc_req)


def AllowVPCSCConfig(project_id, location_id):
  """Allows requests in Remote Repository inside VPC SC perimeter."""
  client = GetClient()
  messages = GetMessages()
  vc = messages.VPCSCConfig(
      name="projects/" + project_id + "/locations/" + location_id +
      "/vpcscConfig",
      vpcscPolicy=messages.VPCSCConfig.VpcscPolicyValueValuesEnum.ALLOW)
  update_vpcsc_req = messages.ArtifactregistryProjectsLocationsUpdateVpcscConfigRequest(
      name="projects/" + project_id + "/locations/" + location_id +
      "/vpcscConfig",
      vPCSCConfig=vc)
  return client.projects_locations.UpdateVpcscConfig(update_vpcsc_req)


def DenyVPCSCConfig(project_id, location_id):
  """Denies requests in Remote Repository inside VPC SC perimeter."""
  client = GetClient()
  messages = GetMessages()
  vc = messages.VPCSCConfig(
      name="projects/" + project_id + "/locations/" + location_id +
      "/vpcscConfig",
      vpcscPolicy=messages.VPCSCConfig.VpcscPolicyValueValuesEnum.DENY)
  get_vpcsc_req = messages.ArtifactregistryProjectsLocationsUpdateVpcscConfigRequest(
      name="projects/" + project_id + "/locations/" + location_id +
      "/vpcscConfig",
      vPCSCConfig=vc)
  return client.projects_locations.UpdateVpcscConfig(get_vpcsc_req)


def EnableUpgradeRedirection(project_id):
  messages = GetMessages()
  return SetUpgradeRedirectionState(
      project_id, messages.ProjectSettings.LegacyRedirectionStateValueValuesEnum
      .REDIRECTION_FROM_GCR_IO_ENABLED)


def DisableUpgradeRedirection(project_id):
  messages = GetMessages()
  return SetUpgradeRedirectionState(
      project_id, messages.ProjectSettings.LegacyRedirectionStateValueValuesEnum
      .REDIRECTION_FROM_GCR_IO_DISABLED)


def FinalizeUpgradeRedirection(project_id):
  messages = GetMessages()
  return SetUpgradeRedirectionState(
      project_id, messages.ProjectSettings.LegacyRedirectionStateValueValuesEnum
      .REDIRECTION_FROM_GCR_IO_FINALIZED)


def SetUpgradeRedirectionState(
    project_id, redirection_state, pull_percent=None
):
  """Sets the upgrade redirection state for the supplied project."""
  client = GetClient()
  messages = GetMessages()
  project_settings = messages.ProjectSettings(
      legacyRedirectionState=redirection_state)
  update_mask = "legacy_redirection_state"
  if pull_percent:
    project_settings.pullPercent = pull_percent
  update_settings_req = (
      messages.ArtifactregistryProjectsUpdateProjectSettingsRequest(
          name="projects/" + project_id + "/projectSettings",
          projectSettings=project_settings,
          updateMask=update_mask,
      )
  )
  return client.projects.UpdateProjectSettings(update_settings_req)
