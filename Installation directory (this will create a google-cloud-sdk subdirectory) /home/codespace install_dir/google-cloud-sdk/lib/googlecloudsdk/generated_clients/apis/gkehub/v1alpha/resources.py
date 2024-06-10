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
"""Resource definitions for Cloud Platform Apis generated from apitools."""

import enum


BASE_URL = 'https://gkehub.googleapis.com/v1alpha/'
DOCS_URL = 'https://cloud.google.com/anthos/multicluster-management/connect/registering-a-cluster'


class Collections(enum.Enum):
  """Collections for all supported apis."""

  PROJECTS = (
      'projects',
      'projects/{projectsId}',
      {},
      ['projectsId'],
      True
  )
  PROJECTS_LOCATIONS = (
      'projects.locations',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_FEATURES = (
      'projects.locations.features',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/features/'
              '{featuresId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_FLEETS = (
      'projects.locations.fleets',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/fleets/'
              '{fleetsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_MEMBERSHIPS = (
      'projects.locations.memberships',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/memberships/'
              '{membershipsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_MEMBERSHIPS_BINDINGS = (
      'projects.locations.memberships.bindings',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/memberships/'
              '{membershipsId}/bindings/{bindingsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_MEMBERSHIPS_RBACROLEBINDINGS = (
      'projects.locations.memberships.rbacrolebindings',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/memberships/'
              '{membershipsId}/rbacrolebindings/{rbacrolebindingsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_NAMESPACES = (
      'projects.locations.namespaces',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/namespaces/'
              '{namespacesId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_NAMESPACES_RBACROLEBINDINGS = (
      'projects.locations.namespaces.rbacrolebindings',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/namespaces/'
              '{namespacesId}/rbacrolebindings/{rbacrolebindingsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_OPERATIONS = (
      'projects.locations.operations',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/operations/'
              '{operationsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_ROLLOUTS = (
      'projects.locations.rollouts',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/rollouts/'
              '{rolloutsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_SCOPES = (
      'projects.locations.scopes',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/scopes/'
              '{scopesId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_SCOPES_NAMESPACES = (
      'projects.locations.scopes.namespaces',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/scopes/'
              '{scopesId}/namespaces/{namespacesId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_SCOPES_NAMESPACES_RESOURCEQUOTAS = (
      'projects.locations.scopes.namespaces.resourcequotas',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/scopes/'
              '{scopesId}/namespaces/{namespacesId}/resourcequotas/'
              '{resourcequotasId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_SCOPES_RBACROLEBINDINGS = (
      'projects.locations.scopes.rbacrolebindings',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/scopes/'
              '{scopesId}/rbacrolebindings/{rbacrolebindingsId}',
      },
      ['name'],
      True
  )

  def __init__(self, collection_name, path, flat_paths, params,
               enable_uri_parsing):
    self.collection_name = collection_name
    self.path = path
    self.flat_paths = flat_paths
    self.params = params
    self.enable_uri_parsing = enable_uri_parsing
