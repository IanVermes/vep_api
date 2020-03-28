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
ADD pyproject.toml poetry.lock ./
RUN python3.8 -m pip install --no-cache-dir --disable-pip-version-check --timeout 100 "poetry==1.0.5" pip
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-root
# Copy webapp code
ADD webvep/ ./code/

# Final step (must be users not root otherwise VEP perl commands fail)
USER vep
WORKDIR $OPT_SRC/ensembl-vep/
