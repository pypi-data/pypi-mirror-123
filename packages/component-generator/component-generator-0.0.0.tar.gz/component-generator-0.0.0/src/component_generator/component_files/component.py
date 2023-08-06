from info_file import START_BLOCK, END_BLOCK

COMPONENT_FILES = {
    # ROOT level
    "${componentName}/Makefile": """
POETRY ?= poetry

_default: test

clean:
	find . -name '__pycache__' | xargs rm -rf
	find . -type f -name "*.pyc" -delete

install-dev:
	$(POETRY) install

install:
	$(POETRY) install  --no-dev

format:
	$(POETRY) run isort .
	$(POETRY) run black .

lint:
	$(POETRY) run isort --check-only .
	$(POETRY) run black --check .
	$(POETRY) run flake8 --config setup.cfg

mypy:
	$(POETRY) run mypy -p ${componentName}

  test:
	$(POETRY) run pytest tests

test-cov:
	$(POETRY) run pytest tests --cov=${componentName}

coverage-report:
	$(POETRY) run coverage xml -i -o coverage.xml
	$(POETRY) run coverage report

test-and-report:
	# we want to report on success AND failure
	make test-cov && make coverage-report || (make coverage-report; exit 1)

.PHONY: clean install install-dev test coverage-report test-and-report

""",
    "${componentName}/Dockerfile": """FROM gcr.io/atlas-images/python-poetry:3.8.8-buster as base

COPY --chown=onnauser:onnagroup ./ /app

FROM base as production
RUN make install
USER root
RUN apt remove -y --purge binutils libc6-dev gcc --allow-remove-essential
USER onnauser

FROM base as test
RUN make install-dev
USER root
RUN apt remove -y --purge binutils libc6-dev gcc --allow-remove-essential
USER onnauser

""",
    "${componentName}/pyproject.toml": """[tool.poetry]
name = "${componentName}"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
pydantic = "^1.8.1"
prometheus-client = "^0.9.0"
onna-utils = "^0.1.0"
onna-types = "^0.1.0"

[tool.poetry.dev-dependencies]
pytest = "^6.2.2"
mypy = "^0.812"
pytest-asyncio = "^0.14.0"
flake8 = "^3.8.4"
isort = "^5.7.0"
black = "^20.8b1"
pytest-cov = "^2.11.1"
async-asgi-testclient = "^1.4.6"


[[tool.poetry.source]]
name = "onna"
url = "http://onna:atlasense@pypi.intra.onna.internal/simple/"
secondary = true

[tool.black]
line-length = 100
target-version = ['py38']
include = '\.pyi?$'
exclude = '''

(
  /(
      \.eggs         # exclude a few common directories in the
    | \.git          # root of the project
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
  )/
  | foo.py           # also separately exclude a file named foo.py in
                     # the root of the project
)
'''

[tool.poetry.scripts]
"""
    + START_BLOCK
    + """

"""
    + END_BLOCK
    + """

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
	""",
    "${componentName}/README.md": """# ${componentName}
Description here!


## Develop

```
make install-dev
```

## Run tests

Run docker compose before running tests:

```
docker-compose up -d
```

```
make test
```

	""",
    "${componentName}/Jenkinsfile": """@Library('onna-library') _

def MAJOR_VERSION = 0
def MINOR_VERSION = 1

node {
  environments.DoCheckout()
  environments.SetGCLOUD()

  // environments.GetAppName() does extra stuff we don't care about
  def appName = "${componentName}"
  def version = "${MAJOR_VERSION}.${MINOR_VERSION}.${env.BUILD_NUMBER}"
  if (env.BRANCH_NAME != 'master') {
    version = "${MAJOR_VERSION}.${MINOR_VERSION + 1}.0-${env.BRANCH_NAME}${env.BUILD_NUMBER}"
  }
  println("Building version ${version}")

  def image = dockerbuilds.BuildDockerImage(appName, env.BRANCH_NAME, env.BUILD_NUMBER, version, ".", null, null, "--target=test")
  def prefixDockerName = appName + '-' + env.BRANCH_NAME + '-' + env.BUILD_NUMBER + '-test'

  stage ('Start Persistent Layers') {
    // none
  }

  stage ('Run Pre-checks') {
    sh("docker run --rm ${image} /bin/bash -c 'make lint && make mypy'")
  }

  def runName = appName + '-' + env.BRANCH_NAME + '-' + env.BUILD_NUMBER + '-test'
  stage("Run Tests") {
    try {
      sh("docker run --name='${runName}' " +
          "${image} /bin/bash -c 'make test-and-report'")
      sh("docker cp ${runName}:/app/coverage.xml .")
      // fix path to source from report
      sh("sed -i 's@\\<source\\>.*@source>${componentName}</source>@g' coverage.xml")

    } catch(Exception e){
      slackSend (
          channel: '#jenkins',
          color: 'danger',
          message: "Jenkins Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) failed in the alltests stage with ${e.message}", to: 'dev@atlasense.com', body: "Please go to ${env.BUILD_URL}.");
      throw e
    } finally {
      sh("docker rm -v ${runName} || true")
    }
  }

  stage("SonarQube") {
    sonarqube.scan(version)
  }

  image = dockerbuilds.BuildDockerImage(appName, env.BRANCH_NAME, env.BUILD_NUMBER, version, ".", null, null, "--target=production")
  image = dockerbuilds.PushDockerImage(appName, env.BRANCH_NAME, env.BUILD_NUMBER, version, image)

  helm.UpdateHelm(appName, env.BRANCH_NAME, env.BUILD_NUMBER, image, version)
  helm.UploadHelm(appName, env.BRANCH_NAME, env.BUILD_NUMBER, version)

  deploy.ComponentDeploy(appName, env.BRANCH_NAME, env.BUILD_NUMBER, version)

  notify.JobDone(appName, env.JOB_BASE_NAME, env.BUILD_NUMBER)

}
""",
    "${componentName}/AUTOUPDATE": "",
    "${componentName}/setup.cfg": """[flake8]
max-line-length = 120
exclude = .eggs

[mypy-prometheus_client.*]
ignore_missing_imports = True

[mypy-uvicorn.*]
ignore_missing_imports = True

[mypy-lru.*]
ignore_missing_imports = True

[isort]
line_length = 100
include_trailing_comma=True
force_grid_wrap=4
use_parentheses=True
force_single_line=False
multi_line_output=3

[mypy]
plugins = pydantic.mypy
mypy_path = stubs
""",
    #
    # 	Tests
    #
    "${componentName}/tests/__init__.py": "",
    "${componentName}/tests/fixtures.py": "",
    "${componentName}/tests/acceptance/__init__.py": "",
    "${componentName}/tests/acceptance/test_service.py": """
def test_it():
	assert True
""",
    "${componentName}/tests/unit/__init__.py": "",
    "${componentName}/tests/unit/test_service.py": """
def test_it():
	assert True
""",
    #
    # 	Python package
    #
    "${componentName}/${componentName}/__init__.py": "",
    "${componentName}/${componentName}/commands.py": """import argparse
import asyncio
import logging

from .settings import Settings

logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description="command runner", add_help=False)
parser.add_argument(
    "-e",
    "--env-file",
    help="Env file",
)


def get_settings() -> Settings:
    arguments, _ = parser.parse_known_args()
    return Settings(_env_file=arguments.env_file)
"""
    + START_BLOCK
    + """

"""
    + END_BLOCK
    + """

	""",
    "${componentName}/${componentName}/settings.py": """
from pydantic import BaseSettings


class Settings(BaseSettings):
    ...

	""",
    #
    # 	Chart
    #
    "charts/${componentName}/Chart.yaml": """apiVersion: v1
appVersion: 1.4.2
description: ${componentName}
name: ${componentName}
sources:
  - https://github.com/atlasense/${componentName}
maintainers:
- name: Platform
  email: platform@onna.com
version: 99999.99999.99999
""",
    "charts/${componentName}/requirements.yaml": """dependencies:
""",
    "charts/${componentName}/values.yaml": """image: IMAGE_TO_REPLACE
pullSecrets: []


"""
    + START_BLOCK
    + """

"""
    + END_BLOCK
    + """
""",
    "charts/${componentName}/templates/_helpers.tpl": """{{/* vim: set filetype=mustache: */}}
{{/* Expand the name of the chart. */}}
{{- define "name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{/* Create a default fully qualified app name. We truncate at 63 chars because . . . */}}
{{- define "fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}""",
    "charts/${componentName}/templates/cm.yaml": """apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ template "name" . }}-config
  namespace: {{ .Release.Namespace }}
  labels:
    service_name: {{ template "name" . }}
    version: {{ .Chart.Version }}
    tier: "backend"
    release: {{ .Release.Name }}
data:
"""
    + START_BLOCK
    + """

"""
    + END_BLOCK
    + """
""",
}
