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
"""Implements the command to upload an SBOM file."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import arg_parsers
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.command_lib.artifacts import sbom_util
from googlecloudsdk.core import log
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Load(base.Command):
  """Upload an SBOM file and create a reference occurrence."""

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES': """\
          To upload an SBOM file at /path/to/sbom.json for a Docker image in Artifact Registry:

          $ {command} --source=/path/to/sbom.json \
              --uri=us-west1-docker.pkg.dev/my-project/my-repository/busy-box@sha256:abcxyz

          To upload an SBOM file at /path/to/sbom.json for a Docker image with a KMS key version to sign the created SBOM reference:

          $ {command} --source=/path/to/sbom.json \
              --uri=us-west1-docker.pkg.dev/my-project/my-repository/busy-box@sha256:abcxyz \
              --kms-key-version=projects/my-project/locations/us-west1/keyRings/my-key-ring/cryptoKeys/my-key/cryptoKeyVersions/1

          To upload an SBOM file at /path/to/sbom.json for a Docker image from a Docker registry:

          $ {command} --source=/path/to/sbom.json \
              --uri=my-docker-registry/my-image@sha256:abcxyz \
              --destination=gs://my-cloud-storage-bucket
          """,
  }

  @staticmethod
  def Args(parser):
    """Set up arguments for this command.

    Args:
      parser: An argparse.ArgumentPaser.
    """
    parser.add_argument(
        '--source',
        metavar='SOURCE',
        required=True,
        default='.',
        help='The SBOM file for uploading.',
    )
    parser.add_argument(
        '--uri',
        metavar='ARTIFACT_URI',
        required=True,
        help="""\
            The URI of the artifact the SBOM is generated from.
            The URI can be a Docker image from any Docker registries. A URI provided with a tag (e.g. `[IMAGE]:[TAG]`) will be resolved into a URI with a digest (`[IMAGE]@sha256:[DIGEST]`).
            When passing an image which is not from Artifact Registry or Container Registry with a tag, only public images can be resolved.
            Also, when passing an image which is not from Artifact Registry or Container Registry, the `--destination` flag is required.
            """,
    )
    parser.add_argument(
        '--kms-key-version',
        default=None,
        help="""\
            Cloud KMS key version to sign the SBOM reference.
            The key version provided should be the resource ID in the format of
            `projects/[KEY_PROJECT_ID]/locations/[LOCATION]/keyRings/[RING_NAME]/cryptoKeys/[KEY_NAME]/cryptoKeyVersions/[KEY_VERSION]`.
            """,
        required=False,
        type=arg_parsers.RegexpValidator(
            r'^projects/[^/]+/locations/[^/]+/keyRings/[^/]+/cryptoKeys/[^/]+/cryptoKeyVersions/[^/]+$',
            (
                'Must be in format of'
                " 'projects/[KEY_PROJECT_ID]/locations/[LOCATION]/keyRings/[RING_NAME]/cryptoKeys/[KEY_NAME]/cryptoKeyVersions/[KEY_VERSION]'"
            ),
        ),
    )

    parser.add_argument(
        '--destination',
        metavar='DESTINATION',
        default=None,
        required=False,
        help="""\
            The storage path will be used to store the SBOM file.
            Currently only supports Cloud Storage paths start with 'gs://'.
        """,
        type=arg_parsers.RegexpValidator(
            r'^gs://.*$', 'Must be in format of gs://[STORAGE_PATH]'
        ),
    )

  def Run(self, args):
    """Run the load command."""
    # Parse file and get the version.
    s = sbom_util.ParseJsonSbom(args.source)
    log.info(
        'Successfully loaded the SBOM file. Format: {0}-{1}.'.format(
            s.sbom_format, s.version
        )
    )

    if not args.uri:
      raise exceptions.InvalidArgumentException(
          'ARTIFACT_URI',
          '--uri is required.',
      )
    # Get information from the artifact.
    a = sbom_util.ProcessArtifact(args.uri)
    log.info(
        (
            'Processed artifact. '
            + 'Project: {0}, Location: {1}, URI: {2}, Digest {3}.'
        ).format(
            a.project, a.location, a.resource_uri, a.digests.get('sha256', '')
        )
    )
    if (
        sbom_util.ARTIFACT_TYPE_OTHER == a.artifact_type
        and not args.destination
    ):
      raise exceptions.InvalidArgumentException(
          'DESTINATION',
          (
              '--destination is required for images not in Artifact Registry or'
              ' Container Registry.'
          ),
      )

    # Upload SBOM to a GCS bucket.
    remote_path = sbom_util.UploadSbomToGCS(
        source=args.source,
        artifact=a,
        sbom=s,
        gcs_path=args.destination,
    )
    log.info('Uploaded the SBOM file at {0}'.format(remote_path))

    # Create occurrence in the same project as the artifact's project.
    # If artifact doesn't have a project (e.g. non AR/GCR images), we will use
    # the current working project.
    project_id = a.project
    if not project_id:
      project_id = args.project or properties.VALUES.core.project.GetOrFail()
      log.info(
          (
              'Failed to get project_id from the artifact URI {0}. Using'
              ' project {1} for occurrence.'
          ).format(args.uri, project_id)
      )
    # Write reference occurrence.
    occurrence_id = sbom_util.WriteReferenceOccurrence(
        artifact=a,
        project_id=project_id,
        storage=remote_path,
        sbom=s,
        kms_key_version=args.kms_key_version,
    )
    log.info('Wrote reference occurrence {0}.'.format(occurrence_id))
    log.status.Print(
        'Uploaded the SBOM file under the resource URI {}.'.format(
            a.GetOccurrenceResourceUri()
        )
    )
