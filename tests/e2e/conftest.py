from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin

import requests
import pytest


DOCKER_COMPOSE_IMAGE = "web"


@pytest.fixture(scope="module")
def wait_for_docker_to_load(module_scoped_container_getter):
    """Wait for the docker-compose image to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    request_session.mount("http://", HTTPAdapter(max_retries=retries))

    service = module_scoped_container_getter.get(DOCKER_COMPOSE_IMAGE).network_info[0]
    port = service.host_port
    base_url = f"http://localhost:{port}/"
    assert request_session.get(base_url)
    return request_session, base_url


@pytest.fixture
def get_response(wait_for_docker_to_load):
    request_session, base_url = wait_for_docker_to_load

    def response_callback(path_url=""):
        concat_url = urljoin(base_url, path_url)
        response = request_session.get(concat_url)
        return response, concat_url

    yield response_callback
