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
"""Golang related utilities."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.command_lib.util.anthos import binary_operations


class PackOperation(binary_operations.BinaryBackedOperation):
  """PackOperation is a wrapper of the package-go-module binary."""

  def __init__(self, **kwargs):
    super(PackOperation, self).__init__(binary='package-go-module', **kwargs)

  def _ParseArgsForCommand(self, module_path, version, source, output,
                           **kwargs):
    args = [
        '--module_path=' + module_path,
        '--version=' + version,
        '--source=' + source,
        '--output=' + output,
    ]
    return args
