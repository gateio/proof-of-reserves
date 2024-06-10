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

"""Hooks for modifying responses for better formatting on gcloud."""

import re


PROVISIONING_TYPE_ABBREVIATIONS = {
    "ADVANCED": "Adv",
    "STANDARD": "Std",
}

STORAGE_POOL_TYPE_ABBREVIATIONS = {
    "hyperdisk-balanced": "HdB",
    "hyperdisk-throughput": "HdT",
}

STORAGE_POOL_TYPE_REGEX = re.compile(r"storagePoolTypes/([a-zA-Z0-9-]+)")

UNKNOWN_TYPE_PLACEHOLDER = "???"

TB = 1 << 40
GB = 1 << 30
TB_IN_GB = 1 << 10


def format_for_listing(pool_list, _):
  """Format existing fields for displaying them in the list response.

  The formatting logic is complicated enough to the point gcloud"s formatter
  is inconvenient to use.

  Args:
    pool_list: list of storage pools.
  Returns:
    the inputted pool list, with the added fields containing new formatting.
  """
  return list(map(_format_single, pool_list))


def _format_single(pool):
  """Format a single pool for displaying it in the list response."""
  _add_types(pool)
  _add_capacity(pool)
  _maybe_add_iops(pool)
  _maybe_add_throughput(pool)

  return pool


def _add_capacity(pool):
  """Add capacity formatting.

  Args:
    pool: the serializable storage pool
  Returns:
    nothing, it changes the input value.
  """
  provisioned_capacity_bytes = int(pool["poolProvisionedCapacityGb"]) * GB
  provisioned_capacity_tb = provisioned_capacity_bytes / TB

  used_capacity_bytes = int(pool["status"]["poolUsedCapacityBytes"])
  used_capacity_tb = used_capacity_bytes / TB

  formatted_capacity = "{:,.1f}/{:,.0f} ({:.1f}%)".format(
      used_capacity_tb,
      provisioned_capacity_tb,
      100 * (used_capacity_bytes / provisioned_capacity_bytes),
  )

  pool["formattedCapacity"] = formatted_capacity


def _maybe_add_iops(pool):
  """Add iops formatting.

  Args:
    pool: the serializable storage pool
  Returns:
    nothing, it changes the input value.
  """
  if not pool.get("poolProvisionedIops"):
    return

  provisioned_iops = int(pool["poolProvisionedIops"])
  used_iops = int(pool["status"]["poolUsedIops"])

  formatted_iops = "{:,}/{:,} ({:.1f}%)".format(
      used_iops, provisioned_iops, 100 * (used_iops / provisioned_iops)
  )

  pool["formattedIops"] = formatted_iops


def _maybe_add_throughput(pool):
  """Add throughput formatting.

  Args:
    pool: the serializable storage pool
  Returns:
    nothing, it changes the input value.
  """
  if not pool.get("poolProvisionedThroughput"):
    return

  provisioned_throughput = int(pool["poolProvisionedThroughput"])
  used_throughput = int(pool["status"]["poolUsedThroughput"])

  formatted_throughput = "{:,}/{:,} (%{:.1f})".format(
      used_throughput,
      provisioned_throughput,
      100 * (used_throughput / provisioned_throughput),
  )

  pool["formattedThroughput"] = formatted_throughput


def _add_types(pool):
  """Add pool type formatting.

  Args:
    pool: the serializable storage pool
  Returns:
    nothing, it changes the input value.
  """
  types = "{}/{}/{}".format(
      _format_pool_type(pool),
      _format_capacity_provisioning_type(pool),
      _format_perf_provisioning_type(pool),
  )

  pool["formattedTypes"] = types


def _format_pool_type(pool):
  """Format pool type.

  Args:
    pool: the serializable storage pool
  Returns:
    the formatted string
  """
  try:
    matched_type = (
        STORAGE_POOL_TYPE_REGEX.search(pool["storagePoolType"]).group(1).lower()
    )
  except IndexError:
    # this is effectively thrown when the regex did not match
    return UNKNOWN_TYPE_PLACEHOLDER

  return STORAGE_POOL_TYPE_ABBREVIATIONS.get(
      matched_type, UNKNOWN_TYPE_PLACEHOLDER
  )


def _format_capacity_provisioning_type(pool):
  """Format capacity provisioning type.

  Args:
    pool: the serializable storage pool
  Returns:
    the abbreviated string
  """
  return PROVISIONING_TYPE_ABBREVIATIONS.get(
      pool["capacityProvisioningType"], UNKNOWN_TYPE_PLACEHOLDER
  )


def _format_perf_provisioning_type(pool):
  """Format performance provisioning type.

  Args:
    pool: the serializable storage pool
  Returns:
    the abbreviated string
  """

  return PROVISIONING_TYPE_ABBREVIATIONS.get(
      pool["performanceProvisioningType"], UNKNOWN_TYPE_PLACEHOLDER
  )
