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
"""Cloud Speech-to-text recognizers list command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.ml.speech import client
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.ml.speech import flags_v2


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Create(base.ListCommand):
  """List Speech-to-text recognizers."""

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    flags_v2.AddLocationArgToParser(parser)
    parser.display_info.AddFormat(
        'table(name.segment(-1):label=NAME,'
        'createTime.date(tz=LOCAL),'
        'updateTime.date(tz=LOCAL),'
        'model,'
        'language_codes.join(sep=","))')

  def Run(self, args):
    location = args.CONCEPTS.location.Parse()
    speech_client = client.SpeechV2Client()
    return speech_client.ListRecognizers(location, limit=args.limit)
