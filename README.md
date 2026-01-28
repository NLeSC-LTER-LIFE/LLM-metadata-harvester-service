# Badges
<!---
| fair-software.nl recommendations | Example Badges |
|:-|:-:|
| [1. Code Repository](https://fair-software.nl/recommendations/repository)       | [![GitHub URL](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/xenon-middleware/xenon-cli) |
| &nbsp;                                                                          | [![GitHub](https://img.shields.io/github/last-commit/xenon-middleware/xenon-cli)](https://github.com/xenon-middleware/xenon-cli) |
| [2. License](https://fair-software.nl/recommendations/license)                  | [![License](https://img.shields.io/github/license/citation-file-format/cff-converter-python)](https://github.com/citation-file-format/cff-converter-python) |
| &nbsp;                                                                          | [![License](https://img.shields.io/github/license/wadpac/GGIR)](https://github.com/wadpac/ggir) |
| [3. Community Registry](https://fair-software.nl/recommendations/registry)      | [![Research Software Directory](https://img.shields.io/badge/rsd-xenon-00a3e3.svg?labelColor=gray&color=00a3e3)](https://research-software.nl/software/xenon) |
| &nbsp;                                                                          | [![PyPI](https://img.shields.io/pypi/v/cffconvert.svg)](https://pypi.org/project/cffconvert) |
| &nbsp;                                                                          | [![bintray](https://img.shields.io/bintray/v/nlesc/xenon/xenon)](https://bintray.com/nlesc/xenon/xenon) |
| [4. Enable Citation](https://fair-software.nl/recommendations/citation)         | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1154130.svg)](https://doi.org/10.5281/zenodo.1154130) |
| [5. Code Quality Checklist](https://fair-software.nl/recommendations/checklist) | [![cii best practices](https://bestpractices.coreinfrastructure.org/projects/1811/badge)](https://bestpractices.coreinfrastructure.org/projects/1811)  |
| **Other**                                                                       | **Badge** |
| Continuous Integration                                                          | [![Build Status](https://travis-ci.org/research-software-directory/research-software-directory.svg?branch=master)](https://travis-ci.org/research-software-directory/research-software-directory) |
| &nbsp;                                                                          | [![Build status](https://ci.appveyor.com/api/projects/status/vki0xma8y7glpt09/branch/master?svg=true)](https://ci.appveyor.com/project/NLeSC/xenon-cli/branch/master)  |
| Code Analysis                                                                   | [![CodeClimate](https://api.codeclimate.com/v1/badges/ed3655f6056f89f5e107/maintainability)](https://codeclimate.com/github/DynaSlum/satsense/maintainability) |
| &nbsp;                                                                          | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6e3836750fe14f34ba85e26956e8ef10)](https://www.codacy.com/app/c-meijer/eEcoLiDAR?utm_source=www.github.com&amp;utm_medium=referral&amp;utm_content=eEcoLiDAR/eEcoLiDAR&amp;utm_campaign=Badge_Grade) |
| &nbsp;                                                                          | [![SonarCloud](https://sonarcloud.io/api/project_badges/measure?project=nlesc%3AXenon&metric=alert_status)](https://sonarcloud.io/dashboard?id=nlesc%3AXenon) |
| Code Coverage                                                                   | [![codecov](https://codecov.io/gh/wadpac/GGIR/branch/master/graph/badge.svg)](https://codecov.io/gh/wadpac/GGIR) |
| &nbsp; | [![SonarCloud](https://sonarcloud.io/api/project_badges/measure?project=xenon-middleware_xenon-grpc&metric=coverage)](https://sonarcloud.io/component_measures?id=xenon-middleware_xenon-grpc&metric=Coverage) |
| &nbsp; | [![Scrutinizer](https://scrutinizer-ci.com/g/NLeSC/mcfly/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/NLeSC/mcfly/statistics/) |
| &nbsp; | [![Coveralls](https://coveralls.io/repos/github/eEcoLiDAR/eEcoLiDAR/badge.svg)](https://coveralls.io/github/eEcoLiDAR/eEcoLiDAR) |
| &nbsp; | [![CodeClimate](https://api.codeclimate.com/v1/badges/ed3655f6056f89f5e107/test_coverage)](https://codeclimate.com/github/DynaSlum/satsense/test_coverage) |
| Documentation                                                                   | [![ReadTheDocs](https://readthedocs.org/projects/xenon-tutorial/badge/?version=latest)](https://xenon-tutorial.readthedocs.io/en/latest/?badge=latest) |

_(Customize these badges with your own links. Check https://shields.io/ to see which badges are available.)_
--->
# Welcome
This repository provides the framework to making LTER-LIFE's LLM based metadata harvester available as a service.

User are expected to provide the name of a supported large language model (currrently these are those offered by OpenAI and Google Gemini), an associated API key, and the url of the metadata to be harvested.

Installation and detals of use are provided below 
<!---
The repository
[https://github.com/NLeSC/template](https://github.com/NLeSC/template) contains
the template for software projects at the Netherlands eScience Center. In
principle, it follows the general recommendations from https://fair-software.nl
for developing research software, while adding details that are specific to the
Netherlands eScience Center. 

When starting a new project, look for GitHub's prompt to use the template as a
starting point.

The template comes with the 5 recommendations from
[fair-software.nl](https://fair-software.nl) predefined as GitHub issues. You'll
see them as soon as you click [``New issue``](/../../issues/new/choose). For each one, click ``Get started``
to instantiate the issue from the issue template.

Once you have the 5 recommendations as issues in your issue list, feel free to
delete
- the corresponding issue templates from
[/.github/ISSUE_TEMPLATE](/.github/ISSUE_TEMPLATE)
- the Welcome section in this README.md
--->
# Documentation for users

## Installation

To run the service users should ensure apptainer is available on their system and

1. Clone this repository
   
   ```bash
   git clone https://github.com/NLeSC-LTER-LIFE/LLM-metadata-harvester-service.git 
   cd LLM-metadata-harvester-service
   ```

2. create and activate a virtual environment (e.g. named llm)
   ```
    python -m venv ./venv/llm python=3.11
    source ./venv/llm/bin/activate    
   ```

3. Install the service
   ```
   pip install -e .
   ```

4. Build the llm_metadata_harvester container
   ```
   cd container
   apptainer build llm_metadata_harvester_service.sif llm_metadata_harvester_service.sif
   ```
   and place it at `/opt/contianers/llm_metadata_harvester_service.sif`
   creating the directory if needed.

5. The service can the be started from the root directory of the repository
   ```
   bash scripts/start-dev.sh
   ```
   and shut down with
   ```
   bash scripts/stop-dev.sh

 ## Usage

 Having installed and started the service, it can be queried via its REST API:

 1. Submitting a request can be done as
```
curl -i -X POST http://localhost:8000/jobs/   -H "Content-Type: application/json"   -d '{
    "model": "gemini-2.5-flash",
    "api_key": "UserAPIkeyForModelMustBeSuppliedHere",
    "url": "https://stac.ecodatacube.eu/veg_quercus.robur_anv.eml/collection.json?.language=en"
  }'
```
which returns
```
{"job_id":"07035c72-a66a-4b49-9196-8109590236d1","status":"queued","result":null,"error":null}
```

2. Job status can be queried using the returned `job_id`
  ```
   curl -s http://localhost:8000/jobs/$JOB_ID
  ```
3. Pure result can be queried as
   ```
   curl -s http://localhost:8000/jobs/$JOB_ID
  ```
  and provides a (nested) JSON return as
  ```
{"status":"SUCCESS","result":{"model":"gemini-2.5-flash","source_url":"https://stac.ecodatacube.eu/veg_quercus.robur_anv.eml/collection.json?.language=en","metadata":{"schema_version":1,"metadata":{"Metadata date":"2000-01-01 to 2020-12-31;","Metadata language":"English;","Responsible organization metadata":"Opengeohub;","Landing page":"https://doi.org/10.5281/zenodo.5887415;","Title":"Actual probability distribution for Quercus robur (2000–2020) in EcoDataCube;","Description":"Actual Natural Vegetation (ANV): probability of occurrence for the Pedunculate oak in its realized environment for the period 2000 - 2033;","Unique Identifier":"https://doi.org/10.5281/zenodo.5887415;","Resource type":"Species Distribution Model (veg_quercus.robur_anv);","Keywords":"Species distribution model, Tree species, Landsat;","Data creator":"Carmelo Bonannella;","Data contact point":"carmelo.bonannella@opengeohub.org;","Data publisher":"Opengeohub;","Spatial coverage":"Implicitly global or unspecified;","Spatial resolution":"N/A;","Spatial reference system":"N/A;","Temporal coverage":"2000-01-01 00:00:00 UTC – 2020-12-31 00:00:00 UTC;","Temporal resolution":"Variable (e.g., 2-4 year intervals for COG files);","License":"CC-BY-SA-4.0;","Access rights":"Openly accessible;","Distribution access URL":"N/A;","Distribution format":"COG (Cloud Optimized GeoTIFF);","Distribution byte size":"N/A;"}},"returncode":0,"stderr":"Extracting full page text...\nExtracting entities from text...\nConverting extracted nodes to metadata...\n"}}
  ```

<!---
- _description of what the software does_
- _notes on how to install_
--->
# Documentation for developers
<!---
- _notes on how to contribute_
--->
# Documentation for maintainers
<!---
- _notes on how to make a release_
--->
