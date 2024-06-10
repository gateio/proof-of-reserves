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
"""Worker-specific printer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from googlecloudsdk.api_lib.run import service
from googlecloudsdk.command_lib.run.printers import k8s_object_printer_util as k8s_util
from googlecloudsdk.command_lib.run.printers import revision_printer
from googlecloudsdk.command_lib.run.printers import traffic_printer
from googlecloudsdk.core.console import console_attr
from googlecloudsdk.core.resource import custom_printer_base as cp

WORKER_PRINTER_FORMAT = 'worker'


# TODO(b/322180968): Once Worker API is ready, replace Service related
# references and replace _BuildWorkerHeader with the method in k8s_util.
class WorkerPrinter(cp.CustomPrinterBase):
  """Prints the run Worker in a custom human-readable format.

  Format specific to Cloud Run workers. Only available on Cloud Run commands
  that print workers.
  """

  def _BuildWorkerHeader(self, record):
    con = console_attr.GetConsoleAttr()
    status = con.Colorize(*record.ReadySymbolAndColor())
    try:
      place = 'region ' + record.region
    except KeyError:
      place = 'namespace ' + record.namespace
    return con.Emphasize(
        '{} {} {} in {}'.format(status, 'Worker', record.name, place)
    )

  def _GetRevisionHeader(self, record):
    header = ''
    if record.status is None:
      header = 'Unknown revision'
    else:
      header = 'Revision {}'.format(record.status.latestCreatedRevisionName)
    return console_attr.GetConsoleAttr().Emphasize(header)

  def _RevisionPrinters(self, record):
    """Adds printers for the revision."""
    return cp.Lines([
        self._GetRevisionHeader(record),
        k8s_util.GetLabels(record.template.labels),
        revision_printer.RevisionPrinter.TransformSpec(record.template),
    ])

  def _GetWorkerSettings(self, record):
    """Adds worker-level values."""
    labels = [
        cp.Labeled([
            ('Binary Authorization', k8s_util.GetBinAuthzPolicy(record)),
            ('Min Instances', GetMinInstances(record)),
        ])
    ]

    breakglass_value = k8s_util.GetBinAuthzBreakglass(record)
    if breakglass_value is not None:
      # Show breakglass even if empty, but only if set. There's no skip_none
      # option so this the workaround.
      breakglass_label = cp.Labeled([
          ('Breakglass Justification', breakglass_value),
      ])
      breakglass_label.skip_empty = False
      labels.append(breakglass_label)
    description = k8s_util.GetDescription(record)
    if description is not None:
      description_label = cp.Labeled([
          ('Description', description),
      ])
      labels.append(description_label)
    return cp.Section(labels)

  def Transform(self, record):
    """Transform a worker into the output structure of marker classes."""
    worker_settings = self._GetWorkerSettings(record)
    fmt = cp.Lines([
        self._BuildWorkerHeader(record),
        k8s_util.GetLabels(record.labels), ' ',
        traffic_printer.TransformRouteFields(record), ' ', worker_settings,
        (' ' if worker_settings.WillPrintOutput() else ''),
        cp.Labeled([(k8s_util.LastUpdatedMessage(record),
                     self._RevisionPrinters(record))]),
        k8s_util.FormatReadyMessage(record)
    ])
    return fmt


def GetMinInstances(record):
  return record.annotations.get(service.SERVICE_MIN_SCALE_ANNOTATION, '')
