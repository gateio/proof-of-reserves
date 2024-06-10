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
"""Shared request hooks for the Dataplex surface."""
from typing import Any
from googlecloudsdk.generated_clients.apis.dataplex.v1 import dataplex_v1_messages as messages


def TransformEntryRootPath(
    unused_ref: str,
    args: Any,
    request: (
        messages.DataplexProjectsLocationsLookupEntryRequest
        | messages.DataplexProjectsLocationsEntryGroupsEntriesGetRequest
    ),
):
  """Transforms the root path from the "." in CLI to empty string expected in API."""
  if args.paths is not None and isinstance(args.paths, list):
    request.paths = list(set(map(lambda p: p if p != '.' else '', args.paths)))
  return request
