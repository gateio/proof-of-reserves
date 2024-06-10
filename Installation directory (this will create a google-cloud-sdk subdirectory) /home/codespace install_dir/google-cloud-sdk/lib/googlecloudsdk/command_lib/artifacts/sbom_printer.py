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
"""Artifacts SBOM reference specific printer."""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from googlecloudsdk.core.resource import custom_printer_base as cp
from googlecloudsdk.core.resource import flattened_printer as fp


SBOM_PRINTER_FORMAT = "sbom"


# pylint: disable=line-too-long
def _GenerateSignedBy(signatures):
  sig = (", ").join(sig.keyid for sig in signatures)
  if sig == "projects/goog-analysis/locations/global/keyRings/sbomAttestor/cryptoKeys/generatedByArtifactAnalysis/cryptoKeyVersions/1":
    return "Artifact Analysis"
  if sig == "projects/goog-analysis-dev/locations/global/keyRings/sbomAttestor/cryptoKeys/generatedByArtifactAnalysis/cryptoKeyVersions/1":
    return "Artifact Analysis Dev"
  return sig


class SbomPrinter(cp.CustomPrinterBase):
  """Prints SBOM reference fields with customized labels in customized order."""

  def Transform(self, sbom_ref):
    printer = fp.FlattenedPrinter()
    printer.AddRecord({"resource_uri": sbom_ref.occ.resourceUri}, delimit=False)
    printer.AddRecord(
        {"location": sbom_ref.occ.sbomReference.payload.predicate.location},
        delimit=False,
    )
    printer.AddRecord({"reference": sbom_ref.occ.name}, delimit=False)
    sig = _GenerateSignedBy(sbom_ref.occ.sbomReference.signatures)
    if sig:
      printer.AddRecord({"signed_by": sig}, delimit=False)
    if "exists" in sbom_ref.file_info:
      printer.AddRecord(
          {"file_exists": sbom_ref.file_info["exists"]}, delimit=False
      )
    if "err_msg" in sbom_ref.file_info:
      printer.AddRecord(
          {"file_err_msg": sbom_ref.file_info["err_msg"]}, delimit=False
      )
