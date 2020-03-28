FROM ensemblorg/ensembl-vep
#############################################################

## Install Python, Poetry, deps and the package as a build step


USER root
WORKDIR $OPT_SRC/ensembl-vep/webvep
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3.8

ENV PYTHONUNBUFFERED 1
# Copy project dep file and install the deps
ADD pyproject.toml poetry.lock ./
RUN python3.8 -m pip install --no-cache-dir --disable-pip-version-check --timeout 100 "poetry==1.0.5" pip
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-root

ADD webvep/ ./code/
# RUN /code/manage.py collectstatic --noinput

# Setup directory for web app


# Install our helpers Poetry & virtualenv


#############################################################
# Final step
USER vep
WORKDIR $OPT_SRC/ensembl-vep/



