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


BASE_URL = 'https://beyondcorp.googleapis.com/v1/'
DOCS_URL = 'https://cloud.google.com/'


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
  PROJECTS_LOCATIONS_APPCONNECTIONS = (
      'projects.locations.appConnections',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/appConnections/'
              '{appConnectionsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_APPCONNECTORS = (
      'projects.locations.appConnectors',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/appConnectors/'
              '{appConnectorsId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_APPGATEWAYS = (
      'projects.locations.appGateways',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/appGateways/'
              '{appGatewaysId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_CLIENTCONNECTORSERVICES = (
      'projects.locations.clientConnectorServices',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/'
              'clientConnectorServices/{clientConnectorServicesId}',
      },
      ['name'],
      True
  )
  PROJECTS_LOCATIONS_CLIENTGATEWAYS = (
      'projects.locations.clientGateways',
      '{+name}',
      {
          '':
              'projects/{projectsId}/locations/{locationsId}/clientGateways/'
              '{clientGatewaysId}',
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

  def __init__(self, collection_name, path, flat_paths, params,
               enable_uri_parsing):
    self.collection_name = collection_name
    self.path = path
    self.flat_paths = flat_paths
    self.params = params
    self.enable_uri_parsing = enable_uri_parsing
