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
"""Scan a container image using the On-Demand Scanning API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import json

from googlecloudsdk.api_lib.ondemandscanning import util as api_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import flags
from googlecloudsdk.command_lib.artifacts import ondemandscanning_util as ods_util
from googlecloudsdk.command_lib.util.anthos import binary_operations
from googlecloudsdk.command_lib.util.apis import arg_utils
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import progress_tracker
from googlecloudsdk.core.updater import local_state
from googlecloudsdk.core.updater import update_manager
from googlecloudsdk.core.util import platforms
import six

# Extract stage messages to constants for convenience.
SCAN_MESSAGE = 'Scanning container image'
EXTRACT_MESSAGE = ('Locally extracting packages and versions from {} '
                   'container image')
RPC_MESSAGE = 'Remotely initiating analysis of packages and versions'
POLL_MESSAGE = 'Waiting for analysis operation to complete'

# Error messages used to fill in for unknown error cases.
EXTRACTION_KILLED_ERROR_TEMPLATE = (
    'Extraction failed: image extraction was either stopped or crashed '
    '(possibly due to a lack of available memory) with exit code '
    '{exit_code}')
UNKNOWN_EXTRACTION_ERROR_TEMPLATE = (
    'Extraction failed: unknown error (exit code: {exit_code})')


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class ScanBeta(base.Command):
  """Perform a vulnerability scan on a container image.

  You can scan a container image in a Google Cloud registry (Artifact Registry
  or Container Registry), or a local container image.

  Reference an image by tag or digest using any of the formats:

    Artifact Registry:
      LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY-ID/IMAGE[:tag]
      LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY-ID/IMAGE@sha256:digest

    Container Registry:
      [LOCATION.]gcr.io/PROJECT-ID/REPOSITORY-ID/IMAGE[:tag]
      [LOCATION.]gcr.io/PROJECT-ID/REPOSITORY-ID/IMAGE@sha256:digest

    Local:
      IMAGE[:tag]
  """

  detailed_help = {
      'DESCRIPTION':
          '{description}',
      'EXAMPLES':
          """\
    Start a scan of a container image stored in Artifact Registry:

        $ {command} us-west1-docker.pkg.dev/my-project/my-repository/busy-box@sha256:abcxyz --remote

    Start a scan of a container image stored in the Container Registry, and perform the analysis in Europe:

        $ {command} eu.gcr.io/my-project/my-repository/my-image:latest --remote --location=europe

    Start a scan of a container image stored locally, and perform the analysis in Asia:

        $ {command} ubuntu:latest --location=asia
    """
  }

  @staticmethod
  def Args(parser):
    flags.GetResourceURIArg().AddToParser(parser)
    flags.GetRemoteFlag().AddToParser(parser)
    flags.GetOnDemandScanningFakeExtractionFlag().AddToParser(parser)
    flags.GetOnDemandScanningLocationFlag().AddToParser(parser)
    flags.GetAdditionalPackageTypesFlag().AddToParser(parser)
    flags.GetExperimentalPackageTypesFlag().AddToParser(parser)
    flags.GetVerboseErrorsFlag().AddToParser(parser)
    base.ASYNC_FLAG.AddToParser(parser)

  def Run(self, args):
    """Runs local extraction then calls ODS with the results.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      AnalyzePackages operation.

    Raises:
      UnsupportedOS: when the command is run on a Windows machine.
    """
    if platforms.OperatingSystem.IsWindows():
      raise ods_util.UnsupportedOS(
          'On-Demand Scanning is not supported on Windows')

    # Verify that the local-extract component is installed, and prompt the user
    # to install it if it's not.
    try:
      # If the user has access to the gcloud components manager, this will
      # prompt the user to install it. If they do not have access, it will
      # instead print the command to install it using a package manager.
      update_manager.UpdateManager.EnsureInstalledAndRestart(['local-extract'])
    except update_manager.MissingRequiredComponentsError:
      # Two possibilities with this error:
      #   1. The user has access to the gcloud components manager but decided
      #      against intalling it.
      #   2. The user does not have access to the gcloud components manager. A
      #      message was printed to the user with the command to install the
      #      component using their package manager (e.g. apt-get).
      raise
    except local_state.InvalidSDKRootError:
      # This happens when gcloud is run locally, but not when distributed.
      pass

    # Construct the object which invokes the `local-extract` component. This
    # might still fail if the binary is run locally.
    cmd = Command()

    # TODO(b/173619679): Validate RESOURCE_URI argument.

    # Dynamically construct the stages based on the --async flag; when
    # --async=true, we do not need a separate poll stage.
    stages = [
        progress_tracker.Stage(
            EXTRACT_MESSAGE.format('remote' if args.remote else 'local'),
            key='extract'),
        progress_tracker.Stage(RPC_MESSAGE, key='rpc')
    ]
    if not args.async_:
      stages += [progress_tracker.Stage(POLL_MESSAGE, key='poll')]

    messages = self.GetMessages()
    with progress_tracker.StagedProgressTracker(
        SCAN_MESSAGE, stages=stages) as tracker:
      # Stage 1) Extract.
      tracker.StartStage('extract')
      operation_result = cmd(
          resource_uri=args.RESOURCE_URI,
          remote=args.remote,
          fake_extraction=args.fake_extraction,
          additional_package_types=args.additional_package_types,
          experimental_package_types=args.experimental_package_types,
          verbose_errors=args.verbose_errors,
      )
      if operation_result.exit_code:
        # Filter out any log messages on std err and only include any actual
        # extraction errors.
        extraction_error = None
        if operation_result.stderr:
          extraction_error = '\n'.join([
              line for line in operation_result.stderr.splitlines()
              if line.startswith('Extraction failed')
          ])
        if not extraction_error:
          if operation_result.exit_code < 0:
            extraction_error = EXTRACTION_KILLED_ERROR_TEMPLATE.format(
                exit_code=operation_result.exit_code,)
          else:
            extraction_error = UNKNOWN_EXTRACTION_ERROR_TEMPLATE.format(
                exit_code=operation_result.exit_code,)
        tracker.FailStage('extract',
                          ods_util.ExtractionFailedError(extraction_error))
        return

      # Parse stdout for the JSON-ified PackageData protos.
      pkgs = []
      for pkg in json.loads(operation_result.stdout):
        pkg_data = messages.PackageData(
            package=pkg['package'],
            version=pkg['version'],
            cpeUri=pkg['cpe_uri'],
        )
        if 'package_type' in pkg:
          pkg_data.packageType = arg_utils.ChoiceToEnum(
              pkg['package_type'],
              messages.PackageData.PackageTypeValueValuesEnum)
        if 'hash_digest' in pkg:
          pkg_data.hashDigest = pkg['hash_digest']
        pkgs += [pkg_data]
      tracker.CompleteStage('extract')

      # Stage 2) Make the RPC to the On-Demand Scanning API.
      tracker.StartStage('rpc')
      op = self.AnalyzePackages(args, pkgs)
      tracker.CompleteStage('rpc')

      # Stage 3) Poll the operation if requested.
      response = None
      if not args.async_:
        tracker.StartStage('poll')
        tracker.UpdateStage('poll', '[{}]'.format(op.name))
        response = self.WaitForOperation(op)
        tracker.CompleteStage('poll')

    if args.async_:
      log.status.Print('Check operation [{}] for status.'.format(op.name))
      return op
    return response

  def AnalyzePackages(self, args, pkgs):
    return api_util.AnalyzePackagesBeta(
        properties.VALUES.core.project.Get(required=True),
        args.location,
        args.RESOURCE_URI,
        pkgs)

  def GetMessages(self):
    return api_util.GetMessages('v1beta1')

  def WaitForOperation(self, op):
    return ods_util.WaitForOperation(op, 'v1beta1')


@base.ReleaseTracks(base.ReleaseTrack.GA)
class ScanGA(ScanBeta):
  """Perform a vulnerability scan on a container image.

  You can scan a container image in a Google Cloud registry (Artifact Registry
  or Container Registry), or a local container image.

  Reference an image by tag or digest using any of the formats:

    Artifact Registry:
      LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY-ID/IMAGE[:tag]
      LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY-ID/IMAGE@sha256:digest

    Container Registry:
      [LOCATION.]gcr.io/PROJECT-ID/REPOSITORY-ID/IMAGE[:tag]
      [LOCATION.]gcr.io/PROJECT-ID/REPOSITORY-ID/IMAGE@sha256:digest

    Local:
      IMAGE[:tag]
  """

  def AnalyzePackages(self, args, pkgs):
    return api_util.AnalyzePackagesGA(
        properties.VALUES.core.project.Get(required=True),
        args.location,
        args.RESOURCE_URI,
        pkgs)

  def GetMessages(self):
    return api_util.GetMessages('v1')

  def WaitForOperation(self, op):
    return ods_util.WaitForOperation(op, 'v1')


class Command(binary_operations.BinaryBackedOperation):
  """Wrapper for call to the Go binary."""

  def __init__(self, **kwargs):
    super(Command, self).__init__(binary='local-extract', **kwargs)

  def _ParseArgsForCommand(self, resource_uri, remote, fake_extraction,
                           additional_package_types, experimental_package_types,
                           verbose_errors, **kwargs):
    args = [
        '--resource_uri=' + resource_uri,
        '--remote=' + six.text_type(remote),
        '--provide_fake_results=' + six.text_type(fake_extraction),
        # Due to backwards compatibility issues between the gcloud command and
        # the local-extract binary, provide a list of all flags to --undefok
        # which were introduced after the first launch. In this way, new
        # versions of the command can invoke old versions of the binary.
        '--undefok=' + ','.join([
            'additional_package_types',
            'verbose_errors',
        ]),
    ]

    package_types = []
    if additional_package_types:
      package_types += additional_package_types
    if experimental_package_types:
      package_types += experimental_package_types

    if package_types:
      args.append('--additional_package_types=' +
                  six.text_type(','.join(package_types)))

    if verbose_errors:
      args.append('--verbose_errors=' + six.text_type(verbose_errors))

    return args
