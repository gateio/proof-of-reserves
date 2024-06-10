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
"""Utility for interacting with vex command group."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import hashlib
import json
import re

from googlecloudsdk.api_lib.artifacts import exceptions as ar_exceptions
from googlecloudsdk.api_lib.container.images import util as gcr_util
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.command_lib.artifacts import docker_util
from googlecloudsdk.core import log
from  googlecloudsdk.core.util.files import FileReader


POSSIBLE_JUSTIFICATION_FLAGS = [
    'component_not_present',
    'vulnerable_code_not_present',
    'vulnerable_code_cannot_be_controlled_by_adversary',
    'vulnerable_code_not_in_execute_path',
    'inline_mitigations_already_exist',
]

POSSIBLE_PRODUCT_STATUS = ['known_affected',
                           'known_not_affected',
                           'fixed',
                           'under_investigation']

POSSIBLE_REMEDIATION_CATEGORIES = [
    'mitigation',
    'no_fix_planned',
    'none_available',
    'vendor_fix',
    'workaround']

WHOLE_IMAGE_REGEX = r'^[^:@\/]+$'


def ParseVexFile(filename, image_uri, version_uri):
  """Reads a vex file and extracts notes.

  Args:
    filename: str, path to the vex file.
    image_uri: uri of the whole image
    version_uri: uri of a specific version

  Returns:
    A list of notes.

  Raises:
    ar_exceptions.InvalidInputValueError if user input is invalid.
  """

  ca_messages = apis.GetMessagesModule('containeranalysis', 'v1')

  try:
    with FileReader(filename) as file:
      vex = json.load(file)
  except ValueError:
    raise ar_exceptions.InvalidInputValueError(
        'Reading json file has failed'
    )
  _Validate(vex)
  name = ''
  namespace = ''
  document = vex.get('document')
  if document is not None:
    publisher = document.get('publisher')
    if publisher is not None:
      name = publisher.get('name')
      namespace = publisher.get('namespace')
  publisher = ca_messages.Publisher(
      name=name,
      publisherNamespace=namespace,
  )

  generic_uri = version_uri if version_uri else image_uri

  productid_to_product_proto_map = {}
  for product_info in vex['product_tree']['branches']:
    artifact_uri = product_info['name']
    artifact_uri = RemoveHTTPS(artifact_uri)
    if image_uri != artifact_uri:
      continue
    product = product_info['product']
    product_id = product['product_id']
    generic_uri = 'https://{}'.format(generic_uri)
    product_proto = ca_messages.Product(
        name=product['name'],
        id=product_id,
        genericUri=generic_uri,
    )
    productid_to_product_proto_map[product_id] = product_proto

  notes = []
  for vuln in vex['vulnerabilities']:
    for status in vuln['product_status']:
      for product_id in vuln['product_status'][status]:
        product = productid_to_product_proto_map.get(product_id)
        if product is None:
          continue
        noteid, note = _MakeNote(
            vuln, status, product, publisher, document, ca_messages
        )
        if version_uri is None:
          noteid = 'image-{}'.format(noteid)
        note = (
            ca_messages.BatchCreateNotesRequest.NotesValue.AdditionalProperty(
                key=noteid, value=note
            )
        )
        notes.append(note)
  return notes, generic_uri


def _Validate(vex):
  """Validates vex file has all needed fields.

  Args:
    vex: json representing a vex document

  Raises:
    ar_exceptions.InvalidInputValueError if user input is invalid.
  """
  product_tree = vex.get('product_tree')
  if product_tree is None:
    raise ar_exceptions.InvalidInputValueError(
        'product_tree is required in csaf document'
    )
  branches = product_tree.get('branches')
  if branches is None:
    raise ar_exceptions.InvalidInputValueError(
        'branches are required in product tree in csaf document'
    )
  if len(branches) < 1:
    raise ar_exceptions.InvalidInputValueError(
        'at least one branch is expected in product tree in csaf document'
    )
  for product in branches:
    name = product.get('name')
    if name is None:
      raise ar_exceptions.InvalidInputValueError(
          'name is required in product tree in csaf document'
      )
    if len(name.split('/')) < 3:
      raise ar_exceptions.InvalidInputValueError(
          'name of product should be artifact path, showing repository,'
          ' project, and package/image'
      )

  vulnerabilities = vex.get('vulnerabilities')
  if vulnerabilities is None:
    raise ar_exceptions.InvalidInputValueError(
        'vulnerabilities are required in csaf document'
    )
  if len(vulnerabilities) < 1:
    log.warning('at least one vulnerability is expected in csaf document')
  for vuln in vulnerabilities:
    _ValidateVulnerability(vuln)


def _ValidateVulnerability(vuln):
  """Validates vulnerability is structured correctly.

  Args:
    vuln: a vulnerability from vex document

  Raises:
    ar_exceptions.InvalidInputValueError if user input is invalid.
  """
  cve_name = vuln.get('cve')
  if cve_name is None:
    raise ar_exceptions.InvalidInputValueError(
        'cve is required in all vulnerabilities in csaf document'
    )
  product_status = vuln.get('product_status')
  if product_status is None:
    raise ar_exceptions.InvalidInputValueError(
        'product_status is required in all vulnerabilities in csaf document'
    )
  if len(product_status) < 1:
    raise ar_exceptions.InvalidInputValueError(
        'at least one status is expected in each vulnerability'
    )
  for status in product_status:
    if status not in POSSIBLE_PRODUCT_STATUS:
      raise ar_exceptions.InvalidInputValueError(
          'Invalid product status passed in {}.  Product status should be one'
          ' of {}'.format(status, POSSIBLE_PRODUCT_STATUS)
      )
  flags = vuln.get('flags')
  if flags is not None:
    for flag in flags:
      label = flag.get('label')
      if label not in POSSIBLE_JUSTIFICATION_FLAGS:
        raise ar_exceptions.InvalidInputValueError(
            'Invalid flag label passed in {}.  Label should be one of {}'
            .format(label, POSSIBLE_JUSTIFICATION_FLAGS)
        )
  remediations = vuln.get('remediations')
  if remediations is not None:
    for remediation in remediations:
      category = remediation.get('category')
      if category not in POSSIBLE_REMEDIATION_CATEGORIES:
        raise ar_exceptions.InvalidInputValueError(
            'Invalid remediation category passed in {}.  Label should be one'
            ' of {}'.format(category, POSSIBLE_REMEDIATION_CATEGORIES)
        )


def _MakeNote(vuln, status, product, publisher, document, msgs):
  """Makes a note.

  Args:
    vuln: vulnerability proto
    status: string of status of vulnerability
    product: product proto
    publisher: publisher proto.
    document: document proto.
    msgs: container analysis messages

  Returns:
    noteid, and note
  """
  state = None
  remediations = []
  desc_note = None
  justification = None
  notes = vuln.get('notes')
  if notes is not None:
    for note in notes:
      if note['category'] == 'description':
        desc_note = note
  if status == 'known_affected':
    state = msgs.Assessment.StateValueValuesEnum.AFFECTED
    remediations = _GetRemediations(vuln, product, msgs)
  elif status == 'known_not_affected':
    state = msgs.Assessment.StateValueValuesEnum.NOT_AFFECTED
    justification = _GetJustifications(vuln, product, msgs)
  elif status == 'fixed':
    state = msgs.Assessment.StateValueValuesEnum.FIXED
  elif status == 'under_investigation':
    state = msgs.Assessment.StateValueValuesEnum.UNDER_INVESTIGATION
  note = msgs.Note(
      vulnerabilityAssessment=msgs.VulnerabilityAssessmentNote(
          title=document['title'],
          publisher=publisher,
          product=product,
          assessment=msgs.Assessment(
              vulnerabilityId=vuln['cve'],
              shortDescription=desc_note['title']
              if desc_note is not None
              else None,
              longDescription=desc_note['text']
              if desc_note is not None
              else None,
              state=state,
              remediations=remediations,
              justification=justification,
          ),
      ),
  )
  key = (
      note.vulnerabilityAssessment.product.genericUri
      + note.vulnerabilityAssessment.assessment.vulnerabilityId
  )
  result = hashlib.md5(key.encode())
  noteid = result.hexdigest()
  return noteid, note


def _GetRemediations(vuln, product, msgs):
  """Get remediations.

  Args:
    vuln: vulnerability proto
    product: product proto
    msgs: container analysis messages

  Returns:
    remediations proto
  """
  remediations = []
  vuln_remediations = vuln.get('remediations')
  if vuln_remediations is None:
    return remediations
  for remediation in vuln_remediations:
    remediation_type = remediation['category']
    remediation_detail = remediation['details']
    remediation_enum = (
        msgs.Remediation.RemediationTypeValueValuesEnum.lookup_by_name(
            remediation_type.upper()
        )
    )
    for product_id in remediation['product_ids']:
      if product_id == product.id:
        remediation = msgs.Remediation(
            remediationType=remediation_enum, details=remediation_detail
        )
        remediations.append(remediation)
  return remediations


def _GetJustifications(vuln, product, msgs):
  """Get justifications.

  Args:
    vuln: vulnerability proto
    product: product proto
    msgs: container analysis messages

  Returns:
    justification proto
  """
  justification_type_as_string = 'justification_type_unspecified'
  justification_type = None
  flags = vuln.get('flags')
  if flags is None:
    return msgs.Justification()
  for flag in flags:
    label = flag.get('label')
    for product_id in flag.get('product_ids'):
      if product_id == product.id:
        justification_type_as_string = label
  enum_dict = (
      msgs.Justification.JustificationTypeValueValuesEnum.to_dict()
  )
  number = enum_dict[justification_type_as_string.upper()]
  justification_type = (
      msgs.Justification.JustificationTypeValueValuesEnum(number)
  )
  justification = msgs.Justification(
      justificationType=justification_type,
  )
  return justification


def ParseGCRUrl(url):
  """Parse GCR URL.

  Args:
    url: gcr url for version, tag or whole image

  Returns:
    strings of project, image url and version url

  Raises:
    ar_exceptions.InvalidInputValueError: If user input is invalid.
  """
  location_map = {
      'us.gcr.io': 'us',
      'gcr.io': 'us',
      'eu.gcr.io': 'europe',
      'asia.gcr.io': 'asia',
  }
  location = None
  project = None
  image = None
  matches = re.match(docker_util.GCR_DOCKER_REPO_REGEX, url)
  if matches:
    location = location_map[matches.group('repo')]
    project = matches.group('project')
    image = matches.group('image')
  matches = re.match(docker_util.GCR_DOCKER_DOMAIN_SCOPED_REPO_REGEX, url)
  if matches:
    location = location_map[matches.group('repo')]
    project = matches.group('project').replace('/', ':', 1)
    image = matches.group('image')
  if not project or not location or not image:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to parse the GCR image.'
    )
  matches = re.match(WHOLE_IMAGE_REGEX, image)
  if matches:
    return project, url, None

  try:
    docker_digest = gcr_util.GetDigestFromName(url)
  except gcr_util.InvalidImageNameError as e:
    raise ar_exceptions.InvalidInputValueError(
        'Failed to resolve digest of the GCR image'
    ) from e
  image_url = super(type(docker_digest), docker_digest).__str__()
  return project, image_url, str(docker_digest)


def RemoveHTTPS(uri):
  prefix = 'https://'
  if uri.startswith(prefix):
    return uri[len(prefix):]
  return uri
