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

"""The command group for the PAM Entitlements CLI."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Entitlements(base.Group):
  """Manage PAM Entitlements.

     The gcloud pam entitlements command group lets you manage Privileged
     Access Manager (PAM) Entitlements.

     ## EXAMPLES

     To display the details of an entitlement with the name entitlement-name,
     run:

     $ {command} describe entitlement-name

     To search and list all entitlements under a parent for which you are a
     requester, run:

     $ {command} search --location parent --caller-access-type grant-requester

     To search and list all entitlements under a parent for which you are a
     approver, run:

     $ {command} search --location parent --caller-access-type grant-approver

     To list all entitlement under a parent,
     run:

     $ {command} list --location parent

  """
