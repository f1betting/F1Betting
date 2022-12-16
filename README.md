<a name="readme-top"></a>

<div>
<h3 align="center">F1Betting</h3>

  <p align="center">
    An API to do bets with your friends about F1 race results!
    <br />
    <a href="https://github.com/f1betting/F1Betting/issues">Report Bug</a>
    ·
    <a href="https://github.com/f1betting/F1Betting/issues">Request Feature</a>
    <br />
    <br />
    <img alt="GitHub tag (latest by date)" src="https://img.shields.io/github/v/tag/f1betting/f1betting?label=Version">
    <br />
    <img alt="SonarCloud coverage" src="https://sonarcloud.io/api/project_badges/measure?project=f1betting_F1Betting&metric=coverage">
    <img alt="SonarCloud quality gate" src="https://sonarcloud.io/api/project_badges/measure?project=f1betting_F1Betting&metric=alert_status">
    <img alt="SonarCloud code smells" src="https://sonarcloud.io/api/project_badges/measure?project=f1betting_F1Betting&metric=code_smells">
    <br />
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/f1betting/F1Betting/python_on_push_master.yml?label=Build&branch=main">
    <img alt="Docker version" src="https://img.shields.io/docker/v/nieko3/f1betting/latest?label=Docker%20version">
  </p>
</div>



<!-- TABLE OF CONTENTS -->

## 📋 Table of contents

- [ℹ️ About The Project](#-about-the-project)
    - [🚧 Built With](#built-with)
- [🔨 Getting Started](#-getting-started)
    - [⚠ Prerequisites](#-prerequisites)
    - [🤖 .env file](#-env-file)
    - [🚢 Running using Docker](#running-using-docker)
    - [🏡 Running locally](#running-locally)
- [🚀 Usage ](#-usage)
- [📜 License](#-license)

<!-- ABOUT THE PROJECT -->

## ℹ️ About The Project

An API to do bets with your friends about F1 race results!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 🚧 Built With

* [![Python]][Python-url]
* [![FastAPI]][FastAPI-url]
* [![MongoDB]][MongoDB-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## 🔨 Getting Started

Below are the instructions for running the API for development and general usage.

### ⚠ Prerequisites

* [F1API](https://github.com/f1betting/F1API) must be running
* A Google Cloud project with OAuth2 credentials configured

### 🤖 .env file

This project requires a .env file. Below is a template of the values it should contain.

````dotenv
# Database config
DB_URI=
DB_NAME=

# URL to F1API (https://github.com/niek-o/F1API)
F1_API=

# Google Cloud project ID
GOOGLE_ID=
````

### 🚢 Running using Docker

1. You can use the docker image from the DockerHub [repository](https://hub.docker.com/r/nieko3/f1betting) using:

   ````shell
   $ docker pull nieko3/f1betting:latest
   ````

2. Run container using:

    ````shell
    $ docker run --env-file ./.env -d --name f1betting -p 8001:80 f1betting:latest
    ````

### 🏡 Running locally

1. Install dependencies with pip using:

   ````shell
   $ pip install -r requirements.txt
   ````

2. Run main.py to start the API using:
   ````shell
   $ python main.py
   ````

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## 🚀 Usage

<img src="docs/screenshot.png">

A swagger browser is included at the ``/docs`` endpoint. Alternatively you can use the ``/redoc`` endpoint if you wish
to use redoc.

_For the OpenAPI specification, please refer
to [OpenAPI.json](https://github.com/f1betting/F1Betting/blob/main/OpenAPI.json)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->

## 📜 License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

[Python-url]: https://python.org

[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi

[FastAPI-url]: https://fastapi.tiangolo.com/

[MongoDB]: https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white

[MongoDB-url]: https://www.mongodb.com/