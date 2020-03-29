FROM ensemblorg/ensembl-vep
#############################################################

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
# Add test code and test with pytest - pytest will exit with 1 if any tests fail
COPY tests/ ./tests/
RUN pytest -o cache_dir=/var/tmp --run-in-docker

# Final step (must be users not root otherwise VEP perl commands fail)
USER vep
WORKDIR $OPT_SRC/ensembl-vep/
