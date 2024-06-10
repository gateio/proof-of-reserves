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
"""Utility for interacting with containeranalysis API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.ondemandscanning import util as ods_util
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.core import exceptions as core_exceptions
from googlecloudsdk.core import resources


class UnsupportedOS(core_exceptions.Error):
  """Raised when the user attempts to scan from an unsupported operation system.

  Note that this is not the same error as when a user initiates a scan on a
  container image, but that image itself has an unsupported OS. In this case,
  the gcloud command itself is running on an unsupported operation system.
  """


class ExtractionFailedError(core_exceptions.Error):
  """Raised when extraction fails."""
  pass


def WaitForOperation(operation, version):
  """Silently waits for the given google.longrunning.Operation to complete.

  Args:
    operation: The operation to poll.
    version: The ODS API version endpoints to use to talk to the Operations
      service.

  Raises:
    apitools.base.py.HttpError: if the request returns an HTTP error

  Returns:
    The response field of the completed operation.
  """
  op_service = ods_util.GetClient(version).projects_locations_operations
  op_resource = resources.REGISTRY.ParseRelativeName(
      operation.name,
      collection='ondemandscanning.projects.locations.operations')
  poller = waiter.CloudOperationPollerNoResources(op_service)
  return waiter.PollUntilDone(poller, op_resource)

