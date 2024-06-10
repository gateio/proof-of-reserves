# -*- coding: utf-8 -*- #
# Copyright 2021 Google LLC. All Rights Reserved.
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
"""Utility for forming settings for gradle."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

SERVICE_ACCOUNT_TEMPLATE = """\
// Move the secret to ~/.gradle.properties
def artifactRegistryMavenSecret = "{password}"

// Insert following snippet into your build.gradle
// see docs.gradle.org/current/userguide/publishing_maven.html

plugins {{
  id "maven-publish"
}}

publishing {{
  repositories {{
    maven {{
      url "https://{location}-maven.pkg.dev/{repo_path}"
      credentials {{
        username = "{username}"
        password = "$artifactRegistryMavenSecret"
      }}
    }}
  }}
}}

repositories {{
  maven {{
    url "https://{location}-maven.pkg.dev/{repo_path}"
    credentials {{
      username = "{username}"
      password = "$artifactRegistryMavenSecret"
    }}
    authentication {{
      basic(BasicAuthentication)
    }}
  }}
}}
"""

SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE = """\
// Move the secret to ~/.gradle.properties
def artifactRegistryMavenSecret = "{password}"

// Insert following snippet into your build.gradle
// see docs.gradle.org/current/userguide/publishing_maven.html

plugins {{
  id "maven-publish"
}}

publishing {{
  repositories {{
    maven {{
      def snapshotURL = "https://{location}-maven.pkg.dev/{repo_path}"
      def releaseURL = "<Paste release URL here>"
      url version.endsWith('SNAPSHOT') ? snapshotURL : releaseURL
      credentials {{
        username = "{username}"
        password = "$artifactRegistryMavenSecret"
      }}
    }}
  }}
}}

repositories {{
  maven {{
    url "https://{location}-maven.pkg.dev/{repo_path}"
    credentials {{
      username = "{username}"
      password = "$artifactRegistryMavenSecret"
    }}
    authentication {{
      basic(BasicAuthentication)
    }}
  }}
}}
"""

SERVICE_ACCOUNT_RELEASE_TEMPLATE = """\
// Move the secret to ~/.gradle.properties
def artifactRegistryMavenSecret = "{password}"

// Insert following snippet into your build.gradle
// see docs.gradle.org/current/userguide/publishing_maven.html

plugins {{
  id "maven-publish"
}}

publishing {{
  repositories {{
    maven {{
      def snapshotURL = "<Paste snapshot URL here>"
      def releaseURL = "https://{location}-maven.pkg.dev/{repo_path}"
      url version.endsWith('SNAPSHOT') ? snapshotURL : releaseURL
      credentials {{
        username = "{username}"
        password = "$artifactRegistryMavenSecret"
      }}
    }}
  }}
}}

repositories {{
  maven {{
    url "https://{location}-maven.pkg.dev/{repo_path}"
    credentials {{
      username = "{username}"
      password = "$artifactRegistryMavenSecret"
    }}
    authentication {{
      basic(BasicAuthentication)
    }}
  }}
}}
"""

NO_SERVICE_ACCOUNT_TEMPLATE = """\
// Insert following snippet into your build.gradle
// see docs.gradle.org/current/userguide/publishing_maven.html

plugins {{
  id "maven-publish"
  id "com.google.cloud.artifactregistry.gradle-plugin" version "{extension_version}"
}}

publishing {{
  repositories {{
    maven {{
      url "artifactregistry://{location}-maven.pkg.dev/{repo_path}"
    }}
  }}
}}

repositories {{
  maven {{
    url "artifactregistry://{location}-maven.pkg.dev/{repo_path}"
  }}
}}
"""

NO_SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE = """\
// Insert following snippet into your build.gradle
// see docs.gradle.org/current/userguide/publishing_maven.html

plugins {{
  id "maven-publish"
  id "com.google.cloud.artifactregistry.gradle-plugin" version "{extension_version}"
}}

publishing {{
  repositories {{
    maven {{
      def snapshotURL = "artifactregistry://{location}-maven.pkg.dev/{repo_path}"
      def releaseURL = "<Paste release URL here>"
      url version.endsWith('SNAPSHOT') ? snapshotURL : releaseURL
    }}
  }}
}}

repositories {{
  maven {{
    url "artifactregistry://{location}-maven.pkg.dev/{repo_path}"
  }}
}}
"""

NO_SERVICE_ACCOUNT_RELEASE_TEMPLATE = """\
// Insert following snippet into your build.gradle
// see docs.gradle.org/current/userguide/publishing_maven.html

plugins {{
  id "maven-publish"
  id "com.google.cloud.artifactregistry.gradle-plugin" version "{extension_version}"
}}

publishing {{
  repositories {{
    maven {{
      def snapshotURL = "<Paste snapshot URL here>"
      def releaseURL = "artifactregistry://{location}-maven.pkg.dev/{repo_path}"
      url version.endsWith('SNAPSHOT') ? snapshotURL : releaseURL
    }}
  }}
}}

repositories {{
  maven {{
    url "artifactregistry://{location}-maven.pkg.dev/{repo_path}"
  }}
}}
"""

