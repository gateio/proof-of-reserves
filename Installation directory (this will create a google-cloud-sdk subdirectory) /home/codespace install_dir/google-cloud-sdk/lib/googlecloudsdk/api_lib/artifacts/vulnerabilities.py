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
"""API for interacting with vulnerabilities."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.containeranalysis import filter_util
from googlecloudsdk.api_lib.containeranalysis import requests


def GetVulnerabilities(project, resource, query):
  """Given image, return vulnerabilities."""
  filter_kinds = ["VULNERABILITY"]
  filter_ca = filter_util.ContainerAnalysisFilter()
  filter_ca.WithKinds(filter_kinds)
  filter_ca.WithResources([resource])
  filter_ca.WithCustomFilter(query)
  occurrences = requests.ListOccurrencesWithFilters(
      project, filter_ca.GetChunkifiedFilters()
  )
  return occurrences


def GetLatestScan(project, resource):
  """Given project and resource, get the last time it was scanned."""
  filter_kinds = ["DISCOVERY"]
  filter_ca = filter_util.ContainerAnalysisFilter()
  filter_ca.WithKinds(filter_kinds)
  filter_ca.WithResources([resource])
  occurrences = requests.ListOccurrencesWithFilters(
      project, filter_ca.GetChunkifiedFilters()
  )
  latest_scan = None
  for occ in occurrences:
    if latest_scan is None:
      latest_scan = occ
      continue
    try:
      if latest_scan.discovery.lastScanTime < occ.discovery.lastScanTime:
        latest_scan = occ
    except AttributeError:
      continue
  return latest_scan



