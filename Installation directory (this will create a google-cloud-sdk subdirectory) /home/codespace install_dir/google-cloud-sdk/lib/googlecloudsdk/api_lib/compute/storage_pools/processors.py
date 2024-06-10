# -*- coding: utf-8 -*- #
# Copyright 2023 Google Inc. All Rights Reserved.
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
"""Argument processors specifically for storage pools."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals


GB = 2**30


def convert_to_gb(size_bytes: int) -> int:
  """Convert size_bytes to GB (2^30).

  Args:
    size_bytes: Size in bytes.

  Returns:
    Size in gibibytes.
  """
  # Converting to decimal to not have any precision issues. Doing so is
  # computationally not cheap, though it is fine for invoking it once
  # for an argument.
  return size_bytes // GB
