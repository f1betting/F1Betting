<a name="readme-top"></a>

<div>
<h3 align="center">F1Betting</h3>

  <p align="center">
    An API to do bets with your friends about F1 race results!
    <br />
    <a href="https://github.com/niek-o/F1Betting/issues">Report Bug</a>
    ·
    <a href="https://github.com/niek-o/F1Betting/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->

## 📋 Table of contents

- [ℹ️ About The Project](#-about-the-project)
    - [🚧 Built With](#built-with)
- [🔨 Getting Started](#-getting-started)
    - [🤖 .env file](#-env-file)
    - [🚢 Running using Docker](#running-using-docker)
    - [🏡 Running locally](#running-locally)
- [🚀 Usage ](#-usage)
- [📜 License](#-license)

<!-- ABOUT THE PROJECT -->

## ℹ️ About The Project

An API to do bets with your friends about F1 race results!

The API uses Google's OAuth2 tokens to handle users, so a Google project Client ID is required.

This project was made to use with [F1API](https://github.com/niek-o/F1API) as part of research for my
internship.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 🚧 Built With

* [![Python]][Python-url]
* [![FastAPI]][FastAPI-url]
* [![MongoDB]][MongoDB-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## 🔨 Getting Started

Below are the instructions for running the API for development and general usage.

### 🤖 .env file

This project requires a .env file. Below is a template of the values it should contain.

````dotenv
# Use | to separate different addresses 
# This field is optional, leave empty if not desired
ALLOWED_HOSTS=localhost|127.0.0.1

DB_URI=
DB_NAME=

# URL to F1API (https://github.com/niek-o/F1API)
F1_API=

GOOGLE_ID=
````

### 🚢 Running using Docker

1. You can use the docker image from the DockerHub [repository](https://hub.docker.com/r/nieko3/f1betting) using:

   ````shell
   $ docker pull nieko3/f1betting:v1.2.0
   ````

2. Run container using:

    ````shell
    $ docker run --env-file ./.env -d --name f1betting -p 8001:80 f1betting:v1.2.0
    ````

### 🏡 Running locally

1. Install depedencies using pip

   ````shell
   $ pip install -r requirements.txt
   ````

2. Use ``uvicorn`` to host the local development server
   ````shell
   $ uvicorn app.main:app --reload --port 8000
   ````

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## 🚀 Usage

A swagger browser is included at the ``/docs`` endpoint. Alternatively you can use the ``/redoc`` endpoint if you wish
to use redoc.

_For the OpenAPI specification, please refer
to [OpenAPI.json](https://github.com/niek-o/F1Betting/blob/main/OpenAPI.json)_

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