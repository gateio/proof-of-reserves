# -*- coding: utf-8 -*- #
# Copyright 2024 Google LLC. All Rights Reserved.
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
"""Utilities for the Cloud Run API."""
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.calliope import base

_API_NAME = 'run'
_GA_API_VERSION = 'v1'
_ALPHA_API_VERSION = 'v2'

RELEASE_TRACK_TO_API_VERSION = {
    base.ReleaseTrack.GA: _GA_API_VERSION,
    base.ReleaseTrack.BETA: _GA_API_VERSION,
    base.ReleaseTrack.ALPHA: _ALPHA_API_VERSION,
}


def GetMessagesModule(release_track=base.ReleaseTrack.GA):
  """Returns the messages module for Run.

  Args:
    release_track: The desired value of the enum
      googlecloudsdk.calliope.base.ReleaseTrack.

  Returns:
    Module containing the definitions of messages for Run.
  """
  return apis.GetMessagesModule(_API_NAME,
                                RELEASE_TRACK_TO_API_VERSION[release_track])


def GetClientInstance(release_track=base.ReleaseTrack.GA):
  """Returns the client instance for Run.

  Args:
    release_track: The desired value of the enum
      googlecloudsdk.calliope.base.ReleaseTrack.

  Returns:
    base_api.BaseApiClient, Client instance for Run.
  """
  return apis.GetClientInstance(_API_NAME,
                                RELEASE_TRACK_TO_API_VERSION[release_track])
