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
"""Utility for handling SBOM files."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import hashlib
import json
import random
import re

from apitools.base.py import encoding
from apitools.base.py import exceptions as apitools_exceptions
from containerregistry.client import docker_creds
from containerregistry.client import docker_name
from containerregistry.client.v2_2 import docker_http as v2_2_docker_http
from containerregistry.client.v2_2 import docker_image as v2_2_image
from containerregistry.client.v2_2 import docker_image_list as v2_2_image_list
from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.api_lib.cloudkms import base as cloudkms_base
from googlecloudsdk.api_lib.container.images import util as gcr_util
from googlecloudsdk.api_lib.containeranalysis import filter_util
from googlecloudsdk.api_lib.containeranalysis import requests as ca_requests
from googlecloudsdk.api_lib.storage import storage_api
from googlecloudsdk.api_lib.storage import storage_util
from googlecloudsdk.command_lib.artifacts import docker_util
from googlecloudsdk.command_lib.artifacts import requests as ar_requests
from googlecloudsdk.command_lib.artifacts import util
from googlecloudsdk.command_lib.projects import util as project_util
from googlecloudsdk.core import log
from googlecloudsdk.core import resources
from googlecloudsdk.core import transports
from googlecloudsdk.core.util import files
import requests
import six
from six.moves import urllib

_SBOM_FORMAT_SPDX = 'spdx'
_SBOM_FORMAT_CYCLONEDX = 'cyclonedx'
_UNSUPPORTED_SBOM_FORMAT_ERROR = (
    'The file is not in a supported SBOM format. '
    + 'Only spdx and cyclonedx are supported.'
)

_SBOM_REFERENCE_PAYLOAD_TYPE = 'application/vnd.in-toto+json'
_SBOM_REFERENCE_TARGET_TYPE = 'https://in-toto.io/Statement/v0.1'
_SBOM_REFERENCE_PREDICATE_TYPE = (
    'https://bcid.corp' + '.google.com/reference/v0.1'
)
_SBOM_REFERENCE_SPDX_MIME_TYPE = 'application/spdx+json'
_SBOM_REFERENCE_DEFAULT_MIME_TYPE = 'application/json'
_SBOM_REFERENCE_CYCLONEDX_MIME_TYPE = 'application/vnd.cyclonedx+json'
_SBOM_REFERENCE_REFERRERID = (
    'https://containeranalysis.googleapis.com/ArtifactAnalysis@v0.1'
)

_SBOM_REFERENCE_SPDX_EXTENSION = 'spdx.json'
_SBOM_REFERENCE_DEFAULT_EXTENSION = 'json'
_SBOM_REFERENCE_CYCLONEDX_EXTENSION = 'bom.json'

_BUCKET_NAME_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
_BUCKET_SUFFIX_LENGTH = 5

_DEFAULT_DOCKER_REGISTRY = 'registry.hub.docker.com'
_DEFAULT_DOCKER_REPOSITORY = 'library'

_REGISTRY_SCHEME_HTTP = 'http'
_REGISTRY_SCHEME_HTTPS = 'https'

ARTIFACT_TYPE_AR_IMAGE = 'artifactregistry'
ARTIFACT_TYPE_GCR_IMAGE = 'gcr'
ARTIFACT_TYPE_OTHER = 'other'


def _ParseSpdx(data):
  """Retrieves version from the given SBOM dict.

  Args:
    data: Parsed json content of an SBOM file.

  Raises:
    ar_exceptions.InvalidInputValueError: If the sbom format is not supported.

  Returns:
    A SbomFile object with metadata of the given sbom.
  """
  spdx_version = data['spdxVersion']
  version = None
  if isinstance(spdx_version, six.string_types):
    r = re.match(r'^SPDX-([0-9]+[.][0-9]+)$', spdx_version)
    if r is not None:
      version = r.group(1)
  if not version:
    raise ar_exceptions.InvalidInputValueError(
        'Unable to read spdxVersion {0}.'.format(spdx_version)
    )

  return SbomFile(sbom_format=_SBOM_FORMAT_SPDX, version=version)


def _ParseCycloneDx(data):
  """Retrieves version from the given SBOM dict.

  Args:
    data: Parsed json content of an SBOM file.

  Raises:
    ar_exceptions.InvalidInputValueError: If the sbom format is not supported.

  Returns:
    A SbomFile object with metadata of the given sbom.
  """
  if 'specVersion' not in data:
    raise ar_exceptions.InvalidInputValueError(
        'Unable to find specVersion in the CycloneDX file.'
    )

  version = None
  if isinstance(data['specVersion'], six.string_types):
    r = re.match(r'^[0-9]+[.][0-9]+$', data['specVersion'])
    if r is not None:
      version = r.group()
  if not version:
    raise ar_exceptions.InvalidInputValueError(
        'Unable to read specVersion {0}.'.format(data['specVersion'].__str__())
    )

  return SbomFile(sbom_format=_SBOM_FORMAT_CYCLONEDX, version=version)


def ParseJsonSbom(file_path):
  """Retrieves information about a docker image based on the fully-qualified name.

  Args:
    file_path: str, The sbom file location.

  Raises:
    ar_exceptions.InvalidInputValueError: If the sbom format is not supported.

  Returns:
    An SbomFile object with metadata of the given sbom.
  """

  try:
    content = files.ReadFileContents(file_path)
    data = json.loads(content)
  except ValueError as e:
    raise ar_exceptions.InvalidInputValueError(
        'The file is not a valid JSON file', e
    )
  except files.Error as e:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to read the sbom file', e
    )
  # Detect if it's spdx or cyclonedx.
  if 'spdxVersion' in data:
    res = _ParseSpdx(data)
  elif data.get('bomFormat') == 'CycloneDX':
    res = _ParseCycloneDx(data)
  else:
    raise ar_exceptions.InvalidInputValueError(_UNSUPPORTED_SBOM_FORMAT_ERROR)
  sha256_digest = hashlib.sha256(six.ensure_binary(content)).hexdigest()
  res.digests['sha256'] = sha256_digest
  return res


def _GetARDockerImage(uri):
  """Retrieves metadata from the given AR docker image.

  Args:
    uri: Uri of the AR docker image.

  Raises:
    ar_exceptions.InvalidInputValueError: If the uri is invalid.

  Returns:
    An Artifact object with metadata of the given artifact.
  """

  image, docker_version = docker_util.DockerUrlToVersion(uri)
  repo = image.docker_repo
  digests = {'sha256': docker_version.digest.replace('sha256:', '')}
  return Artifact(
      resource_uri=docker_version.GetDockerString(),
      project=repo.project,
      location=repo.location,
      digests=digests,
      artifact_type=ARTIFACT_TYPE_AR_IMAGE,
      scheme=_REGISTRY_SCHEME_HTTPS,
  )


def _GetGCRImage(uri):
  """Retrieves information about the given GCR image.

  Args:
    uri: str, The artifact uri.

  Raises:
    ar_exceptions.InvalidInputValueError: If the uri is invalid.

  Returns:
    An Artifact object with metadata of the given artifact.
  """
  location_map = {
      'us.gcr.io': 'us',
      'gcr.io': 'us',
      'eu.gcr.io': 'europe',
      'asia.gcr.io': 'asia',
  }
  # Get digest by using image.
  try:
    docker_digest = gcr_util.GetDigestFromName(uri)
  except gcr_util.InvalidImageNameError as e:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to resolve digest of the GCR image: {}'.format(e)
    )
  project = None
  location = None
  matches = re.match(docker_util.GCR_DOCKER_REPO_REGEX, uri)
  if matches:
    location = location_map[matches.group('repo')]
    project = matches.group('project')
  matches = re.match(docker_util.GCR_DOCKER_DOMAIN_SCOPED_REPO_REGEX, uri)
  if matches:
    location = location_map[matches.group('repo')]
    project = matches.group('project').replace('/', ':', 1)
  if not project or not location:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to parse project and location from the GCR image.'
    )
  return Artifact(
      resource_uri=docker_digest.__str__(),
      project=project,
      location=location,
      digests={'sha256': docker_digest.digest.replace('sha256:', '')},
      artifact_type=ARTIFACT_TYPE_GCR_IMAGE,
      scheme=_REGISTRY_SCHEME_HTTPS,
  )


def _ResolveDockerImageDigest(image):
  """Returns Digest of the given Docker image.

  Lookup registry to get the manifest's digest. If it returns a list of
  manifests, will return the first one.

  Args:
    image: docker_name.Tag or docker_name.Digest, Docker image.

  Returns:
    An str for the digest.
  """
  with v2_2_image_list.FromRegistry(
      basic_creds=docker_creds.Anonymous(),
      name=image,
      transport=transports.GetApitoolsTransport(),
  ) as manifest_list:
    if manifest_list.exists():
      return manifest_list.digest()
  with v2_2_image.FromRegistry(
      basic_creds=docker_creds.Anonymous(),
      name=image,
      transport=transports.GetApitoolsTransport(),
      accepted_mimes=v2_2_docker_http.SUPPORTED_MANIFEST_MIMES,
  ) as v2_2_img:
    if v2_2_img.exists():
      return v2_2_img.digest()

    return None


def _GetDockerImage(uri):
  """Retrieves information about the given docker image.

  Args:
    uri: str, The artifact uri.

  Raises:
    ar_exceptions.InvalidInputValueError: If the artifact is with tag, and it
    can not be resolved by querying the docker http APIs.

  Returns:
    An Artifact object with metadata of the given artifact.
  """
  try:
    image_digest = docker_name.from_string(uri)
    if isinstance(image_digest, docker_name.Digest):
      return Artifact(
          resource_uri=uri,
          digests={'sha256': image_digest.digest.replace('sha256:', '')},
          artifact_type=ARTIFACT_TYPE_OTHER,
          project=None,
          location=None,
          scheme=None,
      )
  except (docker_name.BadNameException,) as e:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to resolve {0}: {1}'.format(uri, str(e))
    )

  image_uri = uri
  if ':' not in uri:
    image_uri = uri + ':latest'
  image_tag = docker_name.Tag(name=image_uri)
  scheme = v2_2_docker_http.Scheme(image_tag.registry)
  try:
    digest = _ResolveDockerImageDigest(image_tag)
  except (
      v2_2_docker_http.V2DiagnosticException,
      requests.exceptions.InvalidURL,
      v2_2_docker_http.BadStateException,
  ) as e:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to resolve {0}: {1}'.format(uri, str(e))
    )
  if not digest:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to resolve {0}.'.format(uri)
    )
  resource_uri = '{registry}/{repo}@{digest}'.format(
      registry=image_tag.registry, repo=image_tag.repository, digest=digest
  )
  return Artifact(
      resource_uri=resource_uri,
      digests={'sha256': digest.replace('sha256:', '')},
      artifact_type=ARTIFACT_TYPE_OTHER,
      project=None,
      location=None,
      scheme=scheme,
  )


def ProcessArtifact(uri):
  """Retrieves information about the given artifact.

  Args:
    uri: str, The artifact uri.

  Raises:
    ar_exceptions.InvalidInputValueError: If the artifact type is unsupported.

  Returns:
    An Artifact object with metadata of the given artifact.
  """

  if docker_util.IsARDockerImage(uri):
    return _GetARDockerImage(uri)
  elif docker_util.IsGCRImage(uri):
    return _GetGCRImage(uri)
  else:
    # Handle as normal docker containers
    try:
      return _GetDockerImage(uri)
    except ar_exceptions.InvalidInputValueError as e:
      log.debug('Failed to resolve the artifact: {}'.format(e))
      return Artifact(
          resource_uri=uri,
          digests={},
          artifact_type=ARTIFACT_TYPE_OTHER,
          project=None,
          location=None,
          scheme=None,
      )


def _RemovePrefix(value, prefix):
  if value.startswith(prefix):
    return value[len(prefix) :]
  return value


def _EnsurePrefix(value, prefix):
  if not value.startswith(prefix):
    value = prefix + value
  return value


def ListSbomReferences(args):
  """Lists SBOM references in a given project.

  Args:
    args: User input arguments.

  Returns:
    List of SBOM references.
  """
  resource = args.resource
  prefix = args.resource_prefix
  dependency = args.dependency

  if (resource and (prefix or dependency)) or (prefix and dependency):
    raise ar_exceptions.InvalidInputValueError(
        'Cannot specify more than one of the flags --dependency,'
        ' --resource and --resource-prefix.'
    )

  filters = filter_util.ContainerAnalysisFilter().WithKinds(['SBOM_REFERENCE'])
  project = util.GetProject(args)

  if dependency:
    dependency_filters = (
        filter_util.ContainerAnalysisFilter()
        .WithKinds(['PACKAGE'])
        .WithCustomFilter(
            'noteProjectId="goog-analysis" AND dependencyPackageName="{}"'
            .format(dependency)
        )
    )

    package_occs = list(
        ca_requests.ListOccurrences(
            project, dependency_filters.GetFilter(), None
        )
    )
    if not package_occs:
      return []

    # Deduplicate image uris, since one image may have multiple package
    # dependencies with the same name but different versions.
    # All AA generated SBOM occurrence resource uris start with 'https://'.
    images = set(_EnsurePrefix(o.resourceUri, 'https://') for o in package_occs)
    filters.WithResources(images)

  if resource:
    resource_uri = _RemovePrefix(resource, 'https://')
    # We want to match the input if the user stores it as uri.
    resource_uris = [
        'https://{}'.format(resource_uri),
        resource_uri,
    ]
    try:
      # Verify image uri and resolve possible tags.
      artifact = ProcessArtifact(resource_uri)
      if resource_uri != artifact.resource_uri:
        # Match the resolved uri if it's different.
        resource_uris = resource_uris + [
            'https://{}'.format(artifact.resource_uri),
            artifact.resource_uri,
        ]
      # Update the project for the request when a specific resource is provided.
      if artifact.project:
        project = artifact.project

    except (ar_exceptions.InvalidInputValueError, docker_name.BadNameException):
      # Failed to process the artifact. Use the uri directly
      log.status.Print(
          'Failed to resolve the artifact. Filter on the URI directly.'
      )
      pass

    filters.WithResources(resource_uris)

  if prefix:
    path_prefix = _RemovePrefix(prefix, 'https://')
    filters.WithResourcePrefixes([
        'https://{}'.format(path_prefix),
        path_prefix,
    ])

  if dependency:
    # Calling ListOccurrencesWithFilters ignoring page_size.
    occs = ca_requests.ListOccurrencesWithFilters(
        project, filters.GetChunkifiedFilters()
    )
  else:
    occs = ca_requests.ListOccurrences(
        project, filters.GetFilter(), args.page_size
    )

  # Verifying GCS can be slow for large amount of occurrences, so we decided to
  # only verify it when `resource` is provided.
  if resource:
    return _VerifyGCSObjects(occs)
  return [SbomReference(occ, {}) for occ in occs]


def _VerifyGCSObjects(occs):
  return [_VerifyGCSObject(occ) for occ in occs]


def _VerifyGCSObject(occ):
  """Verify the existence and the content of a GCS SBOM file object.

  Args:
    occ: SBOM reference occurrence.

  Returns:
    An SbomReference object with the input occurrence and SBOM file information.
  """
  gcs_client = storage_api.StorageClient()
  obj_ref = storage_util.ObjectReference.FromUrl(
      occ.sbomReference.payload.predicate.location
  )

  file_info = {}
  try:
    gcs_client.GetObject(obj_ref)
  except apitools_exceptions.HttpNotFoundError:
    file_info['exists'] = False
  except apitools_exceptions.HttpError as e:
    msg = json.loads(e.content)
    file_info['err_msg'] = msg['error']['message']
  except Exception as e:  # pylint: disable=broad-except
    # Catch everything here since we don't need or want it to block the output.
    # Simply copy the error message into the file information.
    file_info['err_msg'] = str(e)
  else:
    file_info['exists'] = True

    # TODO(b/271564503): Verify SBOM file content and set file_info['verified'].

  return SbomReference(occ, file_info)


def _DefaultGCSBucketName(project_num, location):
  return 'artifactanalysis-{0}-{1}'.format(location, project_num)


def _GetSbomGCSPath(storage_path, resource_uri, sbom):
  uri_encoded = urllib.parse.urlencode({'uri': resource_uri})[4:]
  version = sbom.version.replace('.', '-')
  return ('gs://{storage_path}/{uri_encoded}/sbom/user-{version}.{ext}').format(
      **{
          'storage_path': storage_path.replace('gs://', '').rstrip('/'),
          'uri_encoded': uri_encoded,
          'version': version,
          'ext': sbom.GetExtension(),
      }
  )


def _FindAvailableGCSBucket(default_bucket, project_id, location):
  """Find an appropriate default bucket to store the SBOM file.

  Find a bucket with the same prefix same as the default bucket in the project.
  If no bucket could be found, will start to create a new bucket by
  concatenating the default bucket name and a random suffix.

  Args:
    default_bucket: str, targeting default bucket name for the resource.
    project_id: str, project we will use to store the SBOM.
    location: str, location we will use to store the SBOM.

  Returns:
    bucket_name: str, name of the prepared bucket.
  """
  gcs_client = storage_api.StorageClient()
  buckets = gcs_client.ListBuckets(project=project_id)
  for bucket in buckets:
    log.debug('Verifying bucket {}'.format(bucket.name))
    if not bucket.name.startswith(default_bucket):
      continue
    if bucket.locationType.lower() == 'dual-region':
      log.debug('Skipping dual region bucket {}'.format(bucket.name))
      continue
    if bucket.location.lower() != location.lower():
      log.debug(
          'The bucket {0} has location {1} is not matching {2}.'.format(
              bucket.name, bucket.location.lower(), location.lower()
          )
      )
      continue
    return bucket.name
  # Failed to find a existing bucket to use.
  # Create a new backup bucket with a random suffix.
  bucket_name = default_bucket + '-'
  for _ in range(_BUCKET_SUFFIX_LENGTH):
    bucket_name = bucket_name + random.choice(_BUCKET_NAME_CHARS)
  gcs_client.CreateBucketIfNotExists(
      bucket=bucket_name,
      project=project_id,
      location=location,
      check_ownership=True,
      enable_uniform_level_access=True,
  )

  return bucket_name


def UploadSbomToGCS(source, artifact, sbom, gcs_path=None):
  """Upload an SBOM file onto the GCS bucket in the given project and location.

  Args:
    source: str, the SBOM file location.
    artifact: Artifact, the artifact metadata SBOM file generated from.
    sbom: SbomFile, metadata of the SBOM file.
    gcs_path: str, the GCS location for the SBOm file. If not provided, will use
      the default bucket path of the artifact.

  Returns:
    dest: str, the GCS storage path the file is copied to.
  """
  gcs_client = storage_api.StorageClient()

  if gcs_path:
    dest = _GetSbomGCSPath(gcs_path, artifact.resource_uri, sbom)
  else:
    project_num = project_util.GetProjectNumber(artifact.project)
    bucket_project = artifact.project
    # Make sure we use eu in all bucket queries to match the naming of GCS.
    bucket_location = artifact.location
    if bucket_location == 'europe':
      bucket_location = 'eu'
    default_bucket = _DefaultGCSBucketName(project_num, bucket_location)

    bucket_name = default_bucket
    use_backup_bucket = False
    try:
      # Make sure the bucket exists, and it's in the right project.
      gcs_client.CreateBucketIfNotExists(
          bucket=bucket_name,
          project=bucket_project,
          location=bucket_location,
          check_ownership=True,
      )
    except storage_api.BucketInWrongProjectError:
      # User is given permission to get and use the bucket, but the bucket is
      # not in the correct project. Will fallback to find a backup bucket.
      log.debug('The default bucket is in a wrong project.')
      use_backup_bucket = True
    except apitools_exceptions.HttpForbiddenError:
      # Either user is not having the permission to get the bucket, or the
      # bucket is created by other users in a different project. We will try to
      # see if we can find a backup bucket to use.
      log.debug('The default bucket cannot be accessed.')
      use_backup_bucket = True
    if use_backup_bucket:
      bucket_name = _FindAvailableGCSBucket(
          default_bucket, bucket_project, bucket_location
      )

    log.debug('Using bucket: {}'.format(bucket_name))
    dest = _GetSbomGCSPath(bucket_name, artifact.resource_uri, sbom)

  target_ref = storage_util.ObjectReference.FromUrl(dest)
  gcs_client.CopyFileToGCS(source, target_ref)

  return dest


def _CreateSbomRefNoteIfNotExists(project_id, sbom):
  """Create the SBOM reference note if not exists.

  Args:
    project_id: str, the project we will use to create the note.
    sbom: SbomFile, metadata of the SBOM file.

  Returns:
    A Note object for the targeting SBOM reference note.
  """
  client = ca_requests.GetClient()
  messages = ca_requests.GetMessages()

  note_id = _GetReferenceNoteID(sbom.sbom_format, sbom.version)
  name = resources.REGISTRY.Create(
      collection='containeranalysis.projects.notes',
      projectsId=project_id,
      notesId=note_id,
  ).RelativeName()

  try:
    get_request = messages.ContaineranalysisProjectsNotesGetRequest(name=name)
    note = client.projects_notes.Get(get_request)
  except apitools_exceptions.HttpNotFoundError:
    log.debug('Note not found. Creating note {0}.'.format(name))
    sbom_reference = messages.SBOMReferenceNote(
        format=sbom.sbom_format, version=sbom.version
    )
    new_note = messages.Note(
        kind=messages.Note.KindValueValuesEnum.SBOM_REFERENCE,
        sbomReference=sbom_reference,
    )
    create_request = messages.ContaineranalysisProjectsNotesCreateRequest(
        parent='projects/{project}'.format(project=project_id),
        noteId=note_id,
        note=new_note,
    )
    note = client.projects_notes.Create(create_request)

  log.debug('get note results: {0}'.format(note))
  return note


def _GenerateSbomRefOccurrence(artifact, sbom, note, storage):
  """Create the SBOM reference note if not exists.

  Args:
    artifact: Artifact, the artifact metadata SBOM file generated from.
    sbom: SbomFile, metadata of the SBOM file.
    note: Note, the Note object we will use to attach occurrence.
    storage: str, the path that SBOM is stored remotely.

  Returns:
    An Occurrence object for the SBOM reference.
  """
  messages = ca_requests.GetMessages()

  sbom_digsets = messages.SbomReferenceIntotoPredicate.DigestValue()
  for k, v in sbom.digests.items():
    sbom_digsets.additionalProperties.append(
        messages.SbomReferenceIntotoPredicate.DigestValue.AdditionalProperty(
            key=k,
            value=v,
        )
    )
  predicate = messages.SbomReferenceIntotoPredicate(
      digest=sbom_digsets,
      location=storage,
      mimeType=sbom.GetMimeType(),
      referrerId=_SBOM_REFERENCE_REFERRERID,
  )

  payload = messages.SbomReferenceIntotoPayload(
      predicateType=_SBOM_REFERENCE_PREDICATE_TYPE,
      _type=_SBOM_REFERENCE_TARGET_TYPE,
      predicate=predicate,
  )
  artifact_digests = messages.Subject.DigestValue()
  for k, v in artifact.digests.items():
    artifact_digests.additionalProperties.append(
        messages.Subject.DigestValue.AdditionalProperty(
            key=k,
            value=v,
        )
    )
  sbom_subject = messages.Subject(
      digest=artifact_digests, name=artifact.resource_uri
  )
  payload.subject.append(sbom_subject)

  ref_occ = messages.SBOMReferenceOccurrence(
      payload=payload,
      payloadType=_SBOM_REFERENCE_PAYLOAD_TYPE,
  )
  # ResourceURI stored in Occurrences should have https:// prefix.
  occ = messages.Occurrence(
      sbomReference=ref_occ,
      noteName=note.name,
      resourceUri=artifact.GetOccurrenceResourceUri(),
  )

  return occ


def _GetReferenceNoteID(sbom_format, sbom_version):
  sbom_version_encoded = sbom_version.replace('.', '-')
  return 'sbom-{0}-{1}'.format(sbom_format, sbom_version_encoded)


def _GenerateSbomRefOccurrenceListFilter(artifact, sbom, project_id):
  f = filter_util.ContainerAnalysisFilter()
  f.WithResources([artifact.GetOccurrenceResourceUri()])
  f.WithKinds(['SBOM_REFERENCE'])
  note_id = _GetReferenceNoteID(sbom.sbom_format, sbom.version)
  f.WithCustomFilter(
      'noteId="{0}" AND noteProjectId="{1}"'.format(note_id, project_id)
  )
  return f.GetFilter()


# TODO(b/279744848): use the PAE function of the third_party/dsse.
def _PAE(payload_type, payload):
  """Creates DSSEv1 Pre-Authentication encoding for given type and payload.

  Args:
    payload_type: str, the SBOM reference payload type.
    payload: bytes, the serialized SBOM reference payload.

  Returns:
    A bytes of DSSEv1 Pre-Authentication encoding.
  """

  return b'DSSEv1 %d %b %d %b' % (
      len(payload_type),
      payload_type.encode('utf-8'),
      len(payload),
      payload,
  )


def _SignSbomRefOccurrencePayload(occ, kms_key_version):
  """Add signatures in reference occurrence by using the given kms key.

  Args:
    occ: Occurrence, the SBOM reference occurrence object we want to sign.
    kms_key_version: str, a kms key used to sign the reference occurrence.

  Returns:
    An Occurrence object with signatures added.
  """

  payload_bytes = six.ensure_binary(
      encoding.MessageToJson(occ.sbomReference.payload)
  )
  data = _PAE(occ.sbomReference.payloadType, payload_bytes)

  kms_client = cloudkms_base.GetClientInstance()
  kms_messages = cloudkms_base.GetMessagesModule()
  req = kms_messages.CloudkmsProjectsLocationsKeyRingsCryptoKeysCryptoKeyVersionsAsymmetricSignRequest(  # pylint: disable=line-too-long
      name=kms_key_version,
      asymmetricSignRequest=kms_messages.AsymmetricSignRequest(data=data),
  )
  resp = kms_client.projects_locations_keyRings_cryptoKeys_cryptoKeyVersions.AsymmetricSign(  # pylint: disable=line-too-long
      req
  )
  messages = ca_requests.GetMessages()
  evelope_signature = messages.EnvelopeSignature(
      keyid=kms_key_version, sig=resp.signature
  )

  occ.envelope = messages.Envelope(
      payload=payload_bytes,
      payloadType=occ.sbomReference.payloadType,
      signatures=[evelope_signature],
  )
  occ.sbomReference.signatures.append(evelope_signature)

  return occ


def WriteReferenceOccurrence(
    artifact, project_id, storage, sbom, kms_key_version
):
  """Write the reference occurrence to link the artifact and the SBOM.

  Args:
    artifact: Artifact, the artifact metadata SBOM file generated from.
    project_id: str, the project_id where we will use to store the Occurrence.
    storage: str, the path that SBOM is stored remotely.
    sbom: SbomFile, metadata of the SBOM file.
    kms_key_version: str, the kms key to sign the reference occurrence payload.

  Returns:
    A str for occurrence ID.
  """
  # Check if the note exists or not.
  note = _CreateSbomRefNoteIfNotExists(project_id, sbom)

  # Generate the occurrence.
  occ = _GenerateSbomRefOccurrence(artifact, sbom, note, storage)

  if kms_key_version:
    occ = _SignSbomRefOccurrencePayload(occ, kms_key_version)

  # Check existing occurrence for updates.
  f = _GenerateSbomRefOccurrenceListFilter(artifact, sbom, project_id)
  log.debug('listing occurrence with filter {0}.'.format(f))
  client = ca_requests.GetClient()
  messages = ca_requests.GetMessages()
  occs = ca_requests.ListOccurrences(project_id, f, None)
  log.debug('list successfully: {}'.format(occs))
  old_occ = None
  for o in occs:
    old_occ = o
    break

  # Write the reference occurrence.
  if old_occ:
    log.debug('updating occurrence {0}.'.format(old_occ.name))
    request = messages.ContaineranalysisProjectsOccurrencesPatchRequest(
        name=old_occ.name,
        occurrence=occ,
        updateMask='sbom_reference,envelope',
    )
    occ = client.projects_occurrences.Patch(request)
  else:
    request = messages.ContaineranalysisProjectsOccurrencesCreateRequest(
        occurrence=occ,
        parent='projects/{project}'.format(project=project_id),
    )
    occ = client.projects_occurrences.Create(request)

  log.debug('Used occurrence: {0}.'.format(occ))
  return occ.name


def ExportSbom(args):
  """Export SBOM files for a given AR image.

  Args:
    args: User input arguments.
  """
  if not args.uri:
    raise ar_exceptions.InvalidInputValueError(
        '--uri is required.',
    )

  uri = _RemovePrefix(args.uri, 'https://')
  if docker_util.IsARDockerImage(uri):
    artifact = _GetARDockerImage(uri)
  elif docker_util.IsGCRImage(uri):
    artifact = _GetGCRImage(uri)
    messages = ar_requests.GetMessages()
    settings = ar_requests.GetProjectSettings(artifact.project)
    if (
        settings.legacyRedirectionState
        != messages.ProjectSettings.LegacyRedirectionStateValueValuesEnum.REDIRECTION_FROM_GCR_IO_ENABLED
    ):
      raise ar_exceptions.InvalidInputValueError(
          'This command only supports Artifact Registry. You can enable'
          ' redirection to use gcr.io repositories in Artifact Registry.'
      )
  else:
    raise ar_exceptions.InvalidInputValueError(
        '{} is not an Artifact Registry image.'.format(uri)
    )

  project = util.GetProject(args)
  if artifact.project:
    project = artifact.project
  resp = ca_requests.ExportSbomV1beta1(
      project, 'https://{}'.format(artifact.resource_uri)
  )
  log.status.Print(
      'Exporting the SBOM file for resource {}. Discovery occurrence ID: {}'
      .format(
          artifact.resource_uri,
          resp.discoveryOccurrenceId,
      )
  )


class SbomReference(object):
  """Holder for SBOM reference.

  Properties:
    occ: SBOM reference occurrence.
    file_info: Information of GCS object SBOM file.
  """

  def __init__(self, occ, file_info):
    self._occ = occ
    self._file_info = file_info

  @property
  def occ(self):
    return self._occ

  @property
  def file_info(self):
    return self._file_info


class SbomFile(object):
  """Holder for SBOM file's metadata.

  Properties:
    sbom_format: Data format of the SBOM file.
    version: Version of the SBOM format.
    digests: A dictionary of digests, where key is the algorithm.
  """

  def __init__(self, sbom_format, version):
    self._sbom_format = sbom_format
    self._version = version
    self._digests = dict()

  def GetMimeType(self):
    if self._sbom_format == _SBOM_FORMAT_SPDX:
      return _SBOM_REFERENCE_SPDX_MIME_TYPE
    if self._sbom_format == _SBOM_FORMAT_CYCLONEDX:
      return _SBOM_REFERENCE_CYCLONEDX_MIME_TYPE
    return _SBOM_REFERENCE_DEFAULT_MIME_TYPE

  def GetExtension(self):
    if self._sbom_format == _SBOM_FORMAT_SPDX:
      return _SBOM_REFERENCE_SPDX_EXTENSION
    if self._sbom_format == _SBOM_FORMAT_CYCLONEDX:
      return _SBOM_REFERENCE_CYCLONEDX_EXTENSION
    return _SBOM_REFERENCE_DEFAULT_EXTENSION

  @property
  def digests(self):
    return self._digests

  @property
  def sbom_format(self):
    return self._sbom_format

  @property
  def version(self):
    return self._version


class Artifact(object):
  """Holder for Artifact's metadata.

  Properties:
    resource_uri: str, Uri will be used when storing as a reference occurrence.
    project: str, Project of the artifact.
    location: str, Location of the artifact.
    digests: A dictionary of digests, where key is the algorithm.
    artifact_type: str, Type of the provided artifact.
    scheme: str, Scheme of the registry.
  """

  def __init__(
      self, resource_uri, project, location, digests, artifact_type, scheme
  ):
    self._resource_uri = resource_uri
    self._project = project
    self._location = location
    self._digests = digests
    self._artifact_type = artifact_type
    self._scheme = scheme

  @property
  def resource_uri(self):
    return self._resource_uri

  @property
  def project(self):
    return self._project

  @property
  def location(self):
    return self._location

  @property
  def digests(self):
    return self._digests

  @property
  def artifact_type(self):
    return self._artifact_type

  def GetOccurrenceResourceUri(self):
    if self._scheme is None:
      return self.resource_uri
    return '{scheme}://{uri}'.format(scheme=self._scheme, uri=self.resource_uri)
