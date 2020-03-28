# vep_webapp
Proof of concept for an API and Frontend to support of the ensembl-vep tool


## Setup to run locally

1. Clone this repo & `cd vep_webapp`
2. [Install Poetry](https://python-poetry.org/docs/#installation), as its the
   package manager for this project
3. `$ poetry config virtualenvs.create false && poetry shell` to let Poetry
   create a local env and have it manage it. If the venv doesn't activate
   automatically, do source `.venv/bin/activate`
4. `$ poetry install` to install the Python dependencies
5.  `$ python manage.py runserver 8080`, and go to
    [http://127.0.0.1:8080/](http://127.0.0.1:8080/) in your web-browser


## Setup to run from docker
1. Clone this repo & `cd vep_webapp`, as the docker image is not registered
2. `$ docker-compose up --build`
3. `$ python manage.py runserver 8080`, and go to
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web-browser

## Testing locally

Assuming the docker-compose network was build and that you are setup locally and
running from local environment.

* `pytest --run-e2e` to run all unit, integration and end2end tests

## Testing docker

* Tests are run at build time
