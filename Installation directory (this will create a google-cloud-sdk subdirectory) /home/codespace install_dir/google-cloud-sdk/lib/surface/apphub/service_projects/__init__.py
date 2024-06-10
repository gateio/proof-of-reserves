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
"""The service projects command group for the App Hub CLI."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base


# NOTE: Release track decorators can be used here as well, and would propagate
# to this group's children.
@base.ReleaseTracks(base.ReleaseTrack.GA)
class ServiceProjectsGA(base.Group):
  """Manage App Hub Service Projects.

  Commands for managing App Hub Service Projects.
  """


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class ServiceProjectsAlpha(base.Group):
  """Manage App Hub Service Projects.

  Commands for managing App Hub Service Projects.
  """
