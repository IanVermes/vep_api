FROM ensemblorg/ensembl-vep
#### BUILD SECTION #############################################################

# Put python related project in its own workdir
USER root
WORKDIR $OPT_SRC/ensembl-vep/webvep
## Install Python3.8 and pip
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3.8

# Copy project dep file and install the deps
ENV PYTHONUNBUFFERED 1
ADD pyproject.toml poetry.lock setup.cfg ./
RUN python3.8 -m pip install --no-cache-dir --disable-pip-version-check --timeout 100 "poetry==1.0.5" pip
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root
# Copy webapp code
COPY webvep/ ./webvep/

#### TESTING SECTION ###########################################################

# Add test code and test with pytest - pytest will exit with 1 if any tests fail
USER vep

COPY tests/ ./tests/
ARG IN_DOCKER
ARG VEP_SCRIPT_PATH
ARG VOLUME_PATH

ENV IN_DOCKER="$IN_DOCKER" VEP_SCRIPT_PATH="$VEP_SCRIPT_PATH" VOLUME_PATH="$VOLUME_PATH"
RUN pytest -o cache_dir=/var/tmp --run-in-docker

# Final step (must be users not root otherwise VEP perl commands fail)
WORKDIR $OPT_SRC/ensembl-vep/
