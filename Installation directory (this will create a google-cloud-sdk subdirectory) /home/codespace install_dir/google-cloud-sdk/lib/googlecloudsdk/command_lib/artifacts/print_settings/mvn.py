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
"""Utility for forming settings for maven."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

SERVICE_ACCOUNT_TEMPLATE = """\
<!-- Insert following snippet into your pom.xml -->

<project>
  <distributionManagement>
    <snapshotRepository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </snapshotRepository>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </repository>
  </distributionManagement>

  <repositories>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </repository>
  </repositories>
</project>

<!-- Insert following snippet into your settings.xml -->

<settings>
  <servers>
    <server>
      <id>{server_id}</id>
      <configuration>
        <httpConfiguration>
          <get>
            <usePreemptive>true</usePreemptive>
          </get>
          <head>
            <usePreemptive>true</usePreemptive>
          </head>
          <put>
            <params>
              <property>
                <name>http.protocol.expect-continue</name>
                <value>false</value>
              </property>
            </params>
          </put>
        </httpConfiguration>
      </configuration>
      <username>{username}</username>
      <password>{password}</password>
    </server>
  </servers>
</settings>
"""

NO_SERVICE_ACCOUNT_TEMPLATE = """\
<!-- Insert following snippet into your pom.xml -->

<project>
  <distributionManagement>
    <snapshotRepository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </snapshotRepository>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </repository>
  </distributionManagement>

  <repositories>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </repository>
  </repositories>

  <build>
    <extensions>
      <extension>
        <groupId>com.google.cloud.artifactregistry</groupId>
        <artifactId>artifactregistry-maven-wagon</artifactId>
        <version>{extension_version}</version>
      </extension>
    </extensions>
  </build>
</project>
"""

NO_SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE = """\
<!-- Insert following snippet into your pom.xml -->

<project>
  <distributionManagement>
    <snapshotRepository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </snapshotRepository>
  </distributionManagement>

  <repositories>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
      <releases>
        <enabled>false</enabled>
      </releases>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </repository>
  </repositories>

  <build>
    <extensions>
      <extension>
        <groupId>com.google.cloud.artifactregistry</groupId>
        <artifactId>artifactregistry-maven-wagon</artifactId>
        <version>{extension_version}</version>
      </extension>
    </extensions>
  </build>
</project>
"""

NO_SERVICE_ACCOUNT_RELEASE_TEMPLATE = """\
<!-- Insert following snippet into your pom.xml -->

<project>
  <distributionManagement>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </repository>
  </distributionManagement>

  <repositories>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>
  </repositories>

  <build>
    <extensions>
      <extension>
        <groupId>com.google.cloud.artifactregistry</groupId>
        <artifactId>artifactregistry-maven-wagon</artifactId>
        <version>{extension_version}</version>
      </extension>
    </extensions>
  </build>
</project>
"""

SERVICE_ACCOUNT_SNAPSHOT_TEMPLATE = """\
<!-- Insert following snippet into your pom.xml -->

<project>
  <distributionManagement>
    <snapshotRepository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </snapshotRepository>
  </distributionManagement>

  <repositories>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
      <releases>
        <enabled>false</enabled>
      </releases>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </repository>
  </repositories>
</project>

<!-- Insert following snippet into your settings.xml -->

<settings>
  <servers>
    <server>
      <id>{server_id}</id>
      <configuration>
        <httpConfiguration>
          <get>
            <usePreemptive>true</usePreemptive>
          </get>
          <head>
            <usePreemptive>true</usePreemptive>
          </head>
          <put>
            <params>
              <property>
                <name>http.protocol.expect-continue</name>
                <value>false</value>
              </property>
            </params>
          </put>
        </httpConfiguration>
      </configuration>
      <username>{username}</username>
      <password>{password}</password>
    </server>
  </servers>
</settings>
"""

SERVICE_ACCOUNT_RELEASE_TEMPLATE = """\
<!-- Insert following snippet into your pom.xml -->

<project>
  <distributionManagement>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
    </repository>
  </distributionManagement>

  <repositories>
    <repository>
      <id>{server_id}</id>
      <url>{scheme}://{location}-maven.pkg.dev/{repo_path}</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>
  </repositories>
</project>

<!-- Insert following snippet into your settings.xml -->

<settings>
  <servers>
    <server>
      <id>{server_id}</id>
      <configuration>
        <httpConfiguration>
          <get>
            <usePreemptive>true</usePreemptive>
          </get>
          <head>
            <usePreemptive>true</usePreemptive>
          </head>
          <put>
            <params>
              <property>
                <name>http.protocol.expect-continue</name>
                <value>false</value>
              </property>
            </params>
          </put>
        </httpConfiguration>
      </configuration>
      <username>{username}</username>
      <password>{password}</password>
    </server>
  </servers>
</settings>
"""
