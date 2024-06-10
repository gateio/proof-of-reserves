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
"""Utilities for the parsing ouput for cloud build v2 API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from apitools.base.py import encoding
from googlecloudsdk.api_lib.cloudbuild.v2 import output_util
from googlecloudsdk.core import yaml
from googlecloudsdk.core.resource import custom_printer_base

PRINTER_FORMAT = "tekton"


class TektonPrinter(custom_printer_base.CustomPrinterBase):
  """Print a  PipelineRun or TaskRun in Tekton YAML format."""

  def Transform(self, internal_proto):
    proto = encoding.MessageToDict(internal_proto)
    if "pipelineSpec" in proto or "pipelineRef" in proto:
      yaml_str = self.InternalPRToTektonPR(proto)
      return yaml.dump(yaml_str, round_trip=True)
    elif "taskSpec" in proto or "taskRef" in proto:
      yaml_str = self.InternalTRToTektonPR(proto)
      return yaml.dump(yaml_str, round_trip=True)

  def InternalPRToTektonPR(self, internal):
    """Convert Tekton yaml file into PipelineRun message."""
    pr = {
        "metadata": {},
        "spec": {},
        "status": {},
    }
    # METADATA
    if "name" in internal:
      pr["metadata"]["name"] = output_util.ParseName(
          internal.pop("name"), "pipelinerun"
      )
    if "annotations" in internal:
      pr["metadata"]["annotations"] = internal.pop("annotations")
    # SPEC
    if "params" in internal:
      pr["spec"]["params"] = _TransformParams(internal.pop("params"))
    if "pipelineSpec" in internal:
      pr["spec"]["pipelineSpec"] = _TransformPipelineSpec(
          internal.pop("pipelineSpec")
      )
    elif "pipelineRef" in internal:
      pr["spec"]["pipelineRef"] = _TransformPipelineRef(
          internal.pop("pipelineRef")
      )
    if "timeout" in internal:
      pr["spec"]["timeout"] = internal.pop("timeout")
    if "workspaces" in internal:
      pr["spec"]["workspaces"] = internal.pop("workspaces")
    # STATUS
    if "conditions" in internal:
      conditions = internal.pop("conditions")
      pr["status"]["conditions"] = _TransformConditions(conditions)
    if "startTime" in internal:
      pr["status"]["startTime"] = internal.pop("startTime")
    if "completionTime" in internal:
      pr["status"]["completionTime"] = internal.pop("completionTime")
    if "resolvedPipelineSpec" in internal:
      rps = internal.pop("resolvedPipelineSpec")
      pr["status"]["pipelineSpec"] = _TransformPipelineSpec(rps)
    if "results" in internal:
      pr["status"]["results"] = _TransformPipelineRunResults(
          internal.pop("results")
      )
    if "childReferences" in internal:
      crs = internal.pop("childReferences")
      pr["status"]["childReferences"] = crs
    # TASKRUNTEMPLATE
    if "serviceAccount" in internal:
      pr["taskRunTemplate"] = {
          "serviceAccountName": internal.pop("serviceAccount"),
      }
    return pr

  def InternalTRToTektonPR(self, internal):
    """Convert Internal TR into Tekton yaml."""
    tr = {
        "metadata": {},
        "spec": {},
        "status": {},
    }
    # METADATA
    if "name" in internal:
      tr["metadata"]["name"] = output_util.ParseName(
          internal.pop("name"), "taskrun"
      )
    # SPEC
    if "params" in internal:
      tr["spec"]["params"] = _TransformParams(internal.pop("params"))
    if "taskSpec" in internal:
      tr["spec"]["taskSpec"] = _TransformTaskSpec(internal.pop("taskSpec"))
    elif "taskRef" in internal:
      tr["spec"]["taskRef"] = _TransformTaskRef(internal.pop("taskRef"))
    if "timeout" in internal:
      tr["spec"]["timeout"] = internal.pop("timeout")
    if "workspaces" in internal:
      tr["spec"]["workspaces"] = internal.pop("workspaces")
    if "serviceAccountName" in internal:
      tr["spec"]["serviceAccountName"] = internal.pop("serviceAccountName")
    # STATUS
    if "conditions" in internal:
      tr["status"]["conditions"] = _TransformConditions(
          internal.pop("conditions")
      )
    if "startTime" in internal:
      tr["status"]["startTime"] = internal.pop("startTime")
    if "completionTime" in internal:
      tr["status"]["completionTime"] = internal.pop("completionTime")
    if "resolvedTaskSpec" in internal:
      rts = internal.pop("resolvedTaskSpec")
      tr["status"]["taskSpec"] = _TransformTaskSpec(rts)
    if "steps" in internal:
      tr["status"]["steps"] = internal.pop("steps")
    if "results" in internal:
      tr["status"]["results"] = _TransformTaskRunResults(
          internal.pop("results")
      )
    if "sidecars" in internal:
      tr["status"]["sidecar"] = internal.pop("sidecars")
    return tr


def _TransformPipelineSpec(ps):
  """Convert PipelineSpec into Tekton yaml."""
  pipeline_spec = {}
  if "params" in ps:
    pipeline_spec["params"] = _TransformParamsSpec(ps.pop("params"))
  if "tasks" in ps:
    pipeline_spec["tasks"] = _TransformPipelineTasks(ps.pop("tasks"))
  if "results" in ps:
    pipeline_spec["results"] = _TransformPipelineResults(ps.pop("results"))
  if "finallyTasks" in ps:
    pipeline_spec["finally"] = _TransformPipelineTasks(ps.pop("finallyTasks"))
  if "workspaces" in ps:
    pipeline_spec["workspaces"] = ps.pop("workspaces")
  return pipeline_spec


def _TransformParamsSpec(ps):
  """Convert ParamsSpecs into Tekton yaml."""
  param_spec = []
  for p in ps:
    param = {}
    if "name" in p:
      param["name"] = p.pop("name")
    if "description" in p:
      param["description"] = p.pop("description")
    if "type" in p:
      param["type"] = p.pop("type").lower()
    if "default" in p:
      param["default"] = _TransformParamValue(p.pop("default"))
    if "properties" in p:
      param["properties"] = p.pop("properties")
    param_spec.append(param)
  return param_spec


def _TransformTaskSpec(ts):
  """Convert TaskSpecs into Tekton yaml."""
  task_spec = {}
  if "params" in ts:
    task_spec["params"] = _TransformParamsSpec(ts.pop("params"))
  if "steps" in ts:
    task_spec["steps"] = ts.pop("steps")
  if "stepTemplate" in ts:
    task_spec["stepTemplate"] = ts.pop("stepTemplate")
  if "results" in ts:
    task_spec["results"] = _TransformTaskResults(ts.pop("results"))
  if "sidecars" in ts:
    task_spec["sidecar"] = ts.pop("sidecars")
  if "workspaces" in ts:
    task_spec["workspaces"] = ts.pop("workspaces")
  return task_spec


def _TransformPipelineTasks(ts):
  """Convert PipelineTasks into Tekton yaml."""
  tasks = []
  for task in ts:
    t = {"name": task.get("name", None)}
    if "params" in task:
      t["params"] = _TransformParams(task.pop("params"))
    if "taskSpec" in task:
      task_spec = task.pop("taskSpec").pop("taskSpec")
      t["taskSpec"] = _TransformTaskSpec(task_spec)
    elif "taskRef" in task:
      t["taskRef"] = task.pop("taskRef")
    if "workspaces" in task:
      t["workspaces"] = task.pop("workspaces")
    if "runAfter" in task:
      t["runAfter"] = task.pop("runAfter")
    if "timeout" in task:
      t["timeout"] = task.pop("timeout")
    tasks.append(t)
  return tasks


def _TransformPipelineResults(rs):
  """Convert PipelineResults into Tekton yaml."""
  results = []
  for r in rs:
    result = {}
    if "name" in r:
      result["name"] = r.pop("name")
    if "description" in r:
      result["description"] = r.pop("description")
    if "type" in r:
      result["type"] = r.pop("type").lower()
    if "value" in r:
      result["value"] = _TransformResultValue(r.pop("value"))
    results.append(result)
  return results


def _TransformTaskResults(rs):
  """Convert TaskResults into Tekton yaml."""
  results = []
  for r in rs:
    result = {}
    if "name" in r:
      result["name"] = r.pop("name")
    if "description" in r:
      result["description"] = r.pop("description")
    if "type" in r:
      result["type"] = r.pop("type").lower()
    if "properties" in r:
      result["properties"] = r.pop("properties")
    results.append(result)
  return results


def _TransformPipelineRunResults(rs):
  """Convert PipelineRunResults into Tekton yaml."""
  results = []
  for r in rs:
    result = {}
    if "name" in r:
      result["name"] = r.pop("name")
    if "value" in r:
      result["value"] = _TransformResultValue(r.pop("value"))
    results.append(result)
  return results


def _TransformTaskRunResults(rs):
  """Convert TaskRunResults into Tekton yaml."""
  results = []
  for r in rs:
    result = {}
    if "name" in r:
      result["name"] = r.pop("name")
    if "value" in r:
      result["value"] = _TransformResultValue(r.pop("value"))
    results.append(result)
  return results


def _TransformResultValue(v):
  """Convert ResultValue into Tekton yaml."""
  if "stringVal" in v:
    return v.pop("stringVal")
  if "arrayVal" in v:
    return v.pop("arrayVal")
  if "objectVal" in v:
    return v.pop("objectVal")
  return v


def _TransformParamValue(v):
  """Convert ParamValue into Tekton yaml."""
  if "stringVal" in v:
    return v.pop("stringVal")
  if "arrayVal" in v:
    return v.pop("arrayVal")
  return v


def _TransformParams(ps):
  """Convert Params into Tekton yaml."""
  params = []
  for p in ps:
    param = {}
    if "name" in p:
      param["name"] = p.pop("name")
    if "value" in p:
      param["value"] = _TransformParamValue(p.pop("value"))
    params.append(param)
  return params


def _TransformConditions(cs):
  """Convert Conditions into Tekton yaml."""
  conditions = []
  for c in cs:
    condition = {}
    # Only append the condition if it has a message
    # which indicates the final condition
    if "message" in c:
      condition["message"] = c.pop("message")
      if "lastTransitionTime" in c:
        condition["lastTransitionTime"] = c.pop("lastTransitionTime")
      if "status" in c:
        condition["status"] = c.pop("status").capitalize()
      if "type" in c:
        condition["type"] = c.pop("type").capitalize()
      if "reason" in c:
        condition["reason"] = c.pop("reason")
        conditions.append(condition)
  return conditions


def _TransformChildRefs(crs):
  """Convert ChildReferences into Tekton yaml."""
  child_refs = []
  for cr in crs:
    child_ref = {}
    if "name" in cr:
      child_ref["name"] = cr.pop("name")
    if "pipelineTask" in cr:
      child_ref["pipelineTask"] = cr.pop("pipelineTask")
    child_refs.append(child_ref)
  return child_refs


def _TransformPipelineRef(pr):
  """Convert PipelineRef into Tekton yaml."""
  pipeline_ref = {}
  if "name" in pr:
    pipeline_ref["name"] = pr.pop("name")
  if "resolver" in pr:
    pipeline_ref["resolver"] = pr.pop("resolver")
  if "params" in pr:
    pipeline_ref["params"] = _TransformParams(pr.pop("params"))
  return pipeline_ref


def _TransformTaskRef(tr):
  """Convert TaskRef into Tekton yaml."""
  task_ref = {}
  if "name" in tr:
    task_ref["name"] = tr.pop("name")
  if "resolver" in tr:
    task_ref["resolver"] = tr.pop("resolver")
  if "params" in tr:
    task_ref["params"] = _TransformParams(tr.pop("params"))
  return task_ref
