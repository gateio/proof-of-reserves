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
"""Implements the command to list vulnerabilities from Artifact Registry."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import re
from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.api_lib.artifacts.vulnerabilities import GetLatestScan
from googlecloudsdk.api_lib.artifacts.vulnerabilities import GetVulnerabilities
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.artifacts import docker_util
from googlecloudsdk.command_lib.artifacts import flags
from googlecloudsdk.command_lib.artifacts import format_util


DEFAULT_LIST_FORMAT = """\
     table[box, title="%TITLE%"](
      occurrence.vulnerability.shortDescription:label=CVE,
      occurrence.vulnerability.effectiveSeverity:label=EFFECTIVE_SEVERITY,
      occurrence.vulnerability.cvssScore:label=CVSS:sort=-1:reverse,
      occurrence.vulnerability.packageIssue.fixAvailable:label=FIX_AVAILABLE,
      occurrence.vulnerability.vexAssessment.state:label=VEX_STATUS,
      occurrence.vulnerability.packageIssue.affectedPackage:sort=3:label=PACKAGE,
      occurrence.vulnerability.packageIssue.packageType:label=PACKAGE_TYPE,
      vexScope,
      {}
    )
    """.format(format_util.CONTAINER_ANALYSIS_METADATA_FORMAT)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class List(base.ListCommand):
  """Command for listing vulnerabilities. To see all fields, use --format=json.
  """

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES': """\
        To list vulnerabilities for an artifact, run:

          $ {command} us-east1-docker.pkg.dev/project123/repository123/someimage@sha256:49765698074d6d7baa82f
      """,
  }

  @staticmethod
  def Args(parser):
    flags.GetListURIArg().AddToParser(parser)
    flags.GetVulnerabilitiesOccurrenceFilterFlag().AddToParser(parser)
    parser.display_info.AddFlatten(['occurrence.vulnerability.packageIssue'])
    return

  def Run(self, args):
    occurrence_filter = args.occurrence_filter
    resource, project = self.replaceTags(args.URI)
    latest_scan = GetLatestScan(project, resource)
    self.setTitle(args, latest_scan)
    occurrences = GetVulnerabilities(project, resource, occurrence_filter)
    occurrences = list(occurrences)
    results = []
    if len(occurrences) < 1:
      return {}
    for occ in occurrences:
      vex_scope = ''
      if (
          occ.vulnerability
          and occ.vulnerability.vexAssessment
          and occ.vulnerability.vexAssessment.noteName
      ):
        tokens = occ.vulnerability.vexAssessment.noteName.split('/')
        if tokens[-1].startswith('image-'):
          vex_scope = 'IMAGE'
        else:
          vex_scope = 'DIGEST'
      results.append(VulnerabilityEntry(occ, vex_scope))
    return results

  def replaceTags(self, original_uri):
    updated_uri = original_uri
    if not updated_uri.startswith('https://'):
      updated_uri = 'https://{}'.format(updated_uri)
    found = re.findall(docker_util.DOCKER_URI_REGEX, updated_uri)
    if found:
      resource_uri_str = found[0][2]
      image, version = docker_util.DockerUrlToVersion(resource_uri_str)
      project = image.project
      docker_html_str_digest = 'https://{}'.format(version.GetDockerString())
      updated_uri = re.sub(
          docker_util.DOCKER_URI_REGEX,
          docker_html_str_digest,
          updated_uri,
          1,
      )
      return updated_uri, project
    raise ar_exceptions.InvalidInputValueError(
        'Received invalid URI {}'.format(original_uri)
    )

  def setTitle(self, args, latest_scan):
    title = ''
    if (
        not latest_scan
        or latest_scan.discovery is None
        or latest_scan.discovery.lastScanTime is None
    ):
      title = 'Scan status unknown'
    else:
      last_scan_time = latest_scan.discovery.lastScanTime[:-11]
      title = 'Latest scan was at {}'.format(last_scan_time)
    list_format = DEFAULT_LIST_FORMAT.replace('%TITLE%', title)
    args.GetDisplayInfo().AddFormat(list_format)


class VulnerabilityEntry(object):
  """Holder for an entry of vulnerability list results.

  Properties:
    occurrence: Vulnerability occurrence.
    vex_scope: Scope of the VEX statement.
  """

  def __init__(self, occurrence, vex_scope):
    self._occurrence = occurrence
    self._vex_scope = vex_scope

  @property
  def occurrence(self):
    return self._occurrence

  @property
  def vex_scope(self):
    return self._vex_scope
