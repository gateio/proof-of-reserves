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
"""Utilities for the parsing output for cloud build v2 API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import re


def ParseName(pattern, primitive_type):
  """Parses the name of a pipelineRun/taskRun.

  Args:
    pattern:
      "projects/{project}/locations/{location}/pipelineRuns/{pipeline_run}"
      "projects/{project}/locations/{location}/taskRuns/{task_run}"
    primitive_type: string

  Returns:
    name: string
  """
  if primitive_type == "pipelinerun":
    match = re.match(
        r"projects/([^/]+)/locations/([^/]+)/pipelineRuns/([^/]+)", pattern
    )
    if match:
      return match.group(3)
  elif primitive_type == "taskrun":
    match = re.match(
        r"projects/([^/]+)/locations/([^/]+)/taskRuns/([^/]+)", pattern
    )
    if match:
      return match.group(3)
