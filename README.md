# vep_webapp
Proof of concept for an API and Frontend to support of the ensembl-vep tool


## Setup

1. Clone this repo & `cd vep_webapp`
2. [Install Poetry](https://python-poetry.org/docs/#installation), as its the
   package manager for this project
3. [Install PostGres](https://www.postgresql.org/), v11 or v12 are fine.
4. `$ poetry install` to install the Python dependencies
5. `$ createuser postgres --superuser --password`, press return and enter the
   password `postgres`
6. `$ createdb testvepapi && createdb vepapi`
8. `$ python manage.py migrate`
9. `$ python manage.py createsuperuser --email admin@example.com --username
   admin` and let the password be `password 123`. So secure!
10. `$ python manage.py runserver 8080`, and go to
    [http://127.0.0.1:8080/](http://127.0.0.1:8080/) in your web-browser

