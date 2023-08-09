# FastAPI+ElasticSearch Test task

![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![fastapi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![sqlalchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white)
![docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Testing

![pytest](https://img.shields.io/badge/pytest_asyncio-2496ED?style=for-the-badge&logo=pytest&logoColor=white)
![codecov](https://img.shields.io/codecov/c/github/Umbreella/elasticsearch_test_task?style=for-the-badge&logo=codecov)

## Description

[Task Description](TaskDescription.pdf)

Completed items:

1. Required Methods:
    1. :white_check_mark: Search among documents by arbitrary text query
    2. :white_check_mark: Delete the document from the database and index
       it by the id field
2. Optional requirements:
    1. :white_check_mark: Functional tests
    2. :white_check_mark: Service running in docker
    3. :white_check_mark: Asynchronous calls

## Getting Started

### Dependencies

![postgresql](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![elasticsearch](https://img.shields.io/badge/elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)

### Environment variables

* To run the application:
    * add in **environment variables** PATH to **.env** file
    * overwrite **.env** file
* The list of all environment variables is specified in the **[.env](.env)**

## Docker

1. docker-compose.yml

```docker
version: "3"

services:
    searchus_test_task:
        image: umbreella/searchus_test_task:latest
        container_name: searchus_test_task
    environment:
        - ENV_FILE=.env
    volumes:
        - [env_file]:/usr/src/app/.env
    ports:
        - [your_open_port]:8000
```

* Docker-compose run

```commandline
docker-compose up -d
```

* Open bash in container

```commandline
docker exec --it searchus_test_task bash
```

* Run commands

```commandline
$ alembic upgrade head
```

## Endpoints

* API docs

```commandline
[your_ip_address]/api/docs/
```

* Openapi.json

```commandline
[your_ip_address]/api/docs/json/
```

## Demo

* Environment variables file - [demo/.env.example](demo/.env.example)

* Docker-compose file - [demo/docker-compose.yml](demo/docker-compose.yml)

* Demo run

```commandline
docker-compose -f demo/docker-compose.yml up -d
```

* Filling database

```commandline
docker exec -it fastapi_demo bach

$ python3 load_demo.py
```

## Live Demo

* [https://searchus.umbreella-dev.ru/](https://searchus.umbreella-dev.ru/api/docs/)
