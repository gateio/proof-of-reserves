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
"""Abandons Cloud Deploy release."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import exceptions as apitools_exceptions
from googlecloudsdk.api_lib.clouddeploy import release
from googlecloudsdk.api_lib.util import exceptions as gcloud_exception
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.command_lib.deploy import exceptions as deploy_exceptions
from googlecloudsdk.command_lib.deploy import release_util
from googlecloudsdk.command_lib.deploy import resource_args
from googlecloudsdk.core.console import console_io

_DETAILED_HELP = {
    'DESCRIPTION':
        '{description}',
    'EXAMPLES':
        """ \
  To abandon a release called `test-release` for delivery pipeline `test-pipeline` in region `us-central1`, run:

  $ {command} test-release --delivery-pipeline=test-pipeline --region=us-central1


""",
}


def _CommonArgs(parser):
  """Register flags for this command.

  Args:
    parser: An argparse.ArgumentParser-like object. It is mocked out in order to
      capture some information, but behaves like an ArgumentParser.
  """
  resource_args.AddReleaseResourceArg(parser, positional=True, required=True)


@base.ReleaseTracks(base.ReleaseTrack.ALPHA, base.ReleaseTrack.BETA,
                    base.ReleaseTrack.GA)
class Abandon(base.CreateCommand):
  """Abandons a release.

  After a release is abandoned, no new rollouts can be created from it.

  Rollouts of abandoned releases can't be rolled back to.

  Existing rollouts of abandoned releases will be unaffected.
  """

  detailed_help = _DETAILED_HELP

  @staticmethod
  def Args(parser):
    _CommonArgs(parser)

  @gcloud_exception.CatchHTTPErrorRaiseHTTPException(
      deploy_exceptions.HTTP_ERROR_FORMAT
  )
  def Run(self, args):
    release_ref = args.CONCEPTS.release.Parse()
    try:
      release_obj = release.ReleaseClient().Get(release_ref.RelativeName())
    except apitools_exceptions.HttpError as error:
      raise exceptions.HttpException(error)
    deployed_targets = release_util.ListCurrentDeployedTargets(
        release_ref, release_obj.targetSnapshots)

    console_message = _GetAbandonReleaseMessageString(deployed_targets)
    console_io.PromptContinue(
        message=console_message,
        prompt_string='Are you sure you want to abandon release {}.'.format(
            release_ref.Name()),
        cancel_on_no=True)
    release.ReleaseClient().Abandon(release_obj.name)
    console_io.log.Print('Abandoned release {}'.format(
        release_ref.RelativeName()))


def _GetAbandonReleaseMessageString(deployed_targets):
  if deployed_targets:
    return 'This release is the latest in {} target(s):\n{}\n'.format(
        len(deployed_targets), '\n'.join([
            '- {}'.format(target_ref.RelativeName())
            for target_ref in deployed_targets
        ]))
  return None
