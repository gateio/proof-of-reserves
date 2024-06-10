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
"""Utility for forming Artifact Registry requests around cleanup policies."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import json

from apitools.base.py import encoding as apitools_encoding
from apitools.base.py import exceptions as apitools_exceptions
from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io
from googlecloudsdk.core.util import encoding
from googlecloudsdk.core.util import times
import six


def ParseCleanupPolicy(path):
  """Reads a cleanup policy from a JSON formatted file.

  Args:
    path: str, path to the policy file.

  Returns:
    A dict describing a cleanup policy, matching the proto description.

  Raises:
    InvalidInputValueError: The JSON file could not be parsed or the data does
    not follow the correct schema.
  """
  content = console_io.ReadFromFileOrStdin(path, binary=False)
  try:
    file_policies = json.loads(encoding.Decode(content))
  except ValueError as e:
    raise apitools_exceptions.InvalidUserInputError(
        'Could not read JSON file {}: {}'.format(path, e))
  if not isinstance(file_policies, list):
    raise apitools_exceptions.InvalidUserInputError(
        'Policy file must contain a list of policies.'
    )
  policies = dict()
  for i in range(len(file_policies)):
    policy = file_policies[i]
    if not isinstance(policy, dict):
      raise apitools_exceptions.InvalidUserInputError(
          'Invalid policy at index {}.'.format(i)
      )
    name = policy.get('name')
    if name is None:
      raise ar_exceptions.InvalidInputValueError(
          'Key "name" not found in policy.'
      )
    if name in policies:
      raise ar_exceptions.InvalidInputValueError(
          'Duplicate key "{}" in policy list.'.format(name)
      )
    action = policy.get('action')
    if action is None:
      raise ar_exceptions.InvalidInputValueError(
          'Key "action" not found in policy "{}".'.format(name)
      )
    try:
      action = action.get('type', '')
    except AttributeError as error:
      six.raise_from(
          ar_exceptions.InvalidInputValueError(
              'Invalid action "{}" in policy "{}".'.format(action, name)
          ),
          error,
      )
    condition = policy.get('condition')
    if condition is not None:
      if not isinstance(condition, dict):
        raise ar_exceptions.InvalidInputValueError(
            'Invalid value for "condition" in policy "{}".'.format(name)
        )
      for duration_key in ['versionAge', 'olderThan', 'newerThan']:
        if duration_key in condition:
          seconds = times.ParseDuration(condition[duration_key])
          condition[duration_key] = six.text_type(seconds.total_seconds) + 's'
    most_recent_versions = policy.get('mostRecentVersions')
    if 'condition' not in policy and 'mostRecentVersions' not in policy:
      raise ar_exceptions.InvalidInputValueError(
          'Key "condition" or "mostRecentVersions" not found in policy "{}".'
          .format('name')
      )
    if 'condition' in policy and 'mostRecentVersions' in policy:
      raise ar_exceptions.InvalidInputValueError(
          'Only one of "condition" or "mostRecentVersions" '
          'allowed in policy "{}".'.format(name)
      )
    policies[name] = {
        'id': name,
        'action': action,
        'condition': condition,
        'mostRecentVersions': most_recent_versions,
    }
  return policies


def SetDeleteCleanupPolicyUpdateMask(unused_ref, unused_args, request):
  """Sets update mask for deleting Cleanup Policies."""
  request.updateMask = 'cleanup_policies'
  return request


def RepositoryToCleanupPoliciesResponse(response, unused_args):
  """Formats Cleanup Policies output and displays Dry Run status."""
  if response.cleanupPolicyDryRun:
    log.status.Print('Dry run is enabled.')
  else:
    log.status.Print('Dry run is disabled.')
  if not response.cleanupPolicies:
    return []
  policies = apitools_encoding.MessageToDict(response.cleanupPolicies)
  sorted_policies = sorted(policies.values(), key=lambda p: p['id'])
  for policy in sorted_policies:
    policy['name'] = policy['id']
    del policy['id']
    policy['action'] = {'type': policy['action']}
  return sorted_policies


def DeleteCleanupPolicyFields(unused_ref, args, request):
  removed_policies = args.policynames.split(',')
  remaining_policies = []
  if request.repository.cleanupPolicies:
    for policy in request.repository.cleanupPolicies.additionalProperties:
      if policy.key not in removed_policies:
        remaining_policies.append(policy)
    request.repository.cleanupPolicies.additionalProperties = remaining_policies
  request.updateMask = None
  return request
