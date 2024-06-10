# -*- coding: utf-8 -*- #
# Copyright 2021 Google LLC. All Rights Reserved.
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
"""Utility for forming settings for npm."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

SERVICE_ACCOUNT_TEMPLATE = """\
# Insert the following snippet into your project .npmrc

{configured_registry}=https://{registry_path}
//{registry_path}:always-auth=true

# Insert the following snippet into your user .npmrc

//{registry_path}:_password="{password}"
//{registry_path}:username=_json_key_base64
//{registry_path}:email=not.valid@email.com
"""

NO_SERVICE_ACCOUNT_TEMPLATE = """\
# Insert the following snippet into your project .npmrc

{configured_registry}=https://{registry_path}
//{registry_path}:always-auth=true
"""
