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
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or
   [http://localhost:8000/](http://localhost:8000/) in your web-browser.
4. Your local host may not be my local host!

## Testing from Docker

* Docker compose will run things at build time
* Tests are run at build time
* A few tests that need access to the volume run at run time just before the
  server starts
* **NB!** You need the volumes to be setup, with genomic data & you must have
  `homo_sapiens -y GRCh38` unpacked at the very least as the end2end test calls
  vep against this genome with the example human `.vcf` file.

## Testing the API
Do `$ docker-compose up` to get the server running. I used
[Postman](https://www.postman.com/) to test the API but curl works just as well.

### `/api/ping/` check the server is alive
With curl and POSTing to `/api/ping/` you can get a pong back
`$ curl -H "Content-Type: application/json" --data '{"data": "ping"}' http://localhost:8000/api/ping/`

Returns `{"data":"pong"}` or ```{"data":["field must be `ping`"]}```

### `/api/vcf/` checks filename validity
With curl and POSTing to `/api/vcf/` you can check if the file is valid or not.
`$ curl -F "vcf_file=@homo_sapiens_GRCh38.vcf" http://127.0.0.1:8000/api/vcf/`

Returns `{"is_valid":true}` or `{"is_valid":false}`

### `/api/vep/` checks filename validity
With curl and POSTing to `/api/vep/` you can get the variant effect output of
the VEP program. `curl -F "vcf_file=@homo_sapiens_GRCh38.vcf" http://127.0.0.1:8000/api/vep/`

Returns the formatted json the test required or `{"is_valid":false}` for an invalid file.

## Volumes

My `vep_data` directory lives in my user folder. Hence, in the
`docker-compose.yml` the volume bridge is supplied as follows

```yml
   volumes:
      - $HOME/vep_data:/opt/vep/.vep
```

My `vep_data` was installed and setup by the perl install and directory layout
is as follows.
```
vep_data
├── Plugins
├── drosophila_melanogaster
│   └── 99_BDGP6.28
├── homo_sapiens
│   └── 99_GRCh38
└── rattus_norvegicus
    └── 99_Rnor_6.0
```

## Downloading volumes via docker compose

Very similar to how you might do it with docker.
`$ docker-compose run web perl INSTALL.pl -a cf -s homo_sapiens -y GRCh38`
`$ docker-compose run web perl INSTALL.pl -a cf -s rattus_norvegicus -y Rnor_6.0`
`$ docker-compose run web perl INSTALL.pl -a cf -s drosophila_melanogaster -y BDGP6.28`
