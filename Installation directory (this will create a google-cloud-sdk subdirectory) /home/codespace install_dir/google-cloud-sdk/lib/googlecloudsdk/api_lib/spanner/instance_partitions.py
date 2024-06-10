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
"""Spanner instance partition API helper."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime

from apitools.base.py import list_pager
from cloudsdk.google.protobuf import timestamp_pb2
from googlecloudsdk.api_lib.spanner import response_util
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.core import properties
from googlecloudsdk.core import resources


# The list of pre-defined IAM roles in Spanner.
KNOWN_ROLES = [
    'roles/spanner.admin',
    'roles/spanner.databaseAdmin',
    'roles/spanner.databaseReader',
    'roles/spanner.databaseUser',
    'roles/spanner.viewer',
]

# Timeout to use in ListInstancePartitions for unreachable instance partitions.
UNREACHABLE_INSTANCE_PARTITION_TIMEOUT = datetime.timedelta(seconds=20)

_API_NAME = 'spanner'
_API_VERSION = 'v1'


def Create(
    instance_partition,
    instance,
    config,
    description,
    nodes,
    processing_units=None,
):
  """Create a new instance partition."""
  client = apis.GetClientInstance(_API_NAME, _API_VERSION)
  # Module containing the definitions of messages for the specified API.
  msgs = apis.GetMessagesModule(_API_NAME, _API_VERSION)
  config_ref = resources.REGISTRY.Parse(
      config,
      params={'projectsId': properties.VALUES.core.project.GetOrFail},
      collection='spanner.projects.instanceConfigs',
  )
  instance_ref = resources.REGISTRY.Parse(
      instance,
      params={'projectsId': properties.VALUES.core.project.GetOrFail},
      collection='spanner.projects.instances',
  )
  instance_partition_obj = msgs.InstancePartition(
      config=config_ref.RelativeName(), displayName=description
  )
  if nodes:
    instance_partition_obj.nodeCount = nodes
  elif processing_units:
    instance_partition_obj.processingUnits = processing_units
  req = msgs.SpannerProjectsInstancesInstancePartitionsCreateRequest(
      parent=instance_ref.RelativeName(),
      createInstancePartitionRequest=msgs.CreateInstancePartitionRequest(
          instancePartitionId=instance_partition,
          instancePartition=instance_partition_obj,
      ),
  )
  return client.projects_instances_instancePartitions.Create(req)


def Get(instance_partition, instance):
  """Get an instance partition by name."""
  client = apis.GetClientInstance(_API_NAME, _API_VERSION)
  msgs = apis.GetMessagesModule(_API_NAME, _API_VERSION)
  ref = resources.REGISTRY.Parse(
      instance_partition,
      params={
          'projectsId': properties.VALUES.core.project.GetOrFail,
          'instancesId': instance,
      },
      collection='spanner.projects.instances.instancePartitions',
  )
  req = msgs.SpannerProjectsInstancesInstancePartitionsGetRequest(
      name=ref.RelativeName()
  )
  return client.projects_instances_instancePartitions.Get(req)


def Patch(
    instance_partition,
    instance,
    description=None,
    nodes=None,
    processing_units=None,
):
  """Update an instance partition."""
  fields = []
  if description is not None:
    fields.append('displayName')
  if nodes is not None:
    fields.append('nodeCount')
  if processing_units is not None:
    fields.append('processingUnits')

  client = apis.GetClientInstance(_API_NAME, _API_VERSION)
  msgs = apis.GetMessagesModule(_API_NAME, _API_VERSION)

  instance_partition_obj = msgs.InstancePartition(displayName=description)
  if processing_units:
    instance_partition_obj.processingUnits = processing_units
  elif nodes:
    instance_partition_obj.nodeCount = nodes

  ref = resources.REGISTRY.Parse(
      instance_partition,
      params={
          'projectsId': properties.VALUES.core.project.GetOrFail,
          'instancesId': instance,
      },
      collection='spanner.projects.instances.instancePartitions',
  )
  req = msgs.SpannerProjectsInstancesInstancePartitionsPatchRequest(
      name=ref.RelativeName(),
      updateInstancePartitionRequest=msgs.UpdateInstancePartitionRequest(
          fieldMask=','.join(fields), instancePartition=instance_partition_obj
      ),
  )
  return client.projects_instances_instancePartitions.Patch(req)


def List(instance_ref):
  """List instance partitions in the project."""
  client = apis.GetClientInstance(_API_NAME, _API_VERSION)
  msgs = apis.GetMessagesModule(_API_NAME, _API_VERSION)
  tp_proto = timestamp_pb2.Timestamp()
  tp_proto.FromDatetime(
      datetime.datetime.now(tz=datetime.timezone.utc)
      + UNREACHABLE_INSTANCE_PARTITION_TIMEOUT
  )
  req = msgs.SpannerProjectsInstancesInstancePartitionsListRequest(
      parent=instance_ref.RelativeName(),
      instancePartitionDeadline=tp_proto.ToJsonString(),
  )
  return list_pager.YieldFromList(
      client.projects_instances_instancePartitions,
      req,
      field='instancePartitions',
      batch_size_attribute='pageSize',
      get_field_func=response_util.GetFieldAndLogUnreachable,
  )


def Delete(instance_partition, instance):
  """Delete an instance partition."""
  client = apis.GetClientInstance(_API_NAME, _API_VERSION)
  msgs = apis.GetMessagesModule(_API_NAME, _API_VERSION)
  ref = resources.REGISTRY.Parse(
      instance_partition,
      params={
          'projectsId': properties.VALUES.core.project.GetOrFail,
          'instancesId': instance,
      },
      collection='spanner.projects.instances.instancePartitions',
  )
  req = msgs.SpannerProjectsInstancesInstancePartitionsDeleteRequest(
      name=ref.RelativeName()
  )
  return client.projects_instances_instancePartitions.Delete(req)
