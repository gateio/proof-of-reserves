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
"""Command group for Container Registry to Artifact Registry upgrade."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.GA)
class Upgrade(base.Group):
  r"""Commands to support Container Registry to Artifact Registry upgrade.

  To print an equivalent Artifact Registry IAM policy for 'gcr.io/my-project':

      $ {command} print-iam-policy gcr.io --project=my-project

  To migrate a project from Container Registry to Artifact Registry using gcr.io
  repos:

      $ {command} migrate --projects=my-project

  To migrate a project from Container Registry to Artifact Registry using
  pkg.dev repos:

      $ {command} migrate --from-gcr-io=gcr.io/from-project \
        --to-pkg-dev=to-project/to-repo
  """

  category = base.CI_CD_CATEGORY
