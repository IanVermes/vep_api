from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import requests
import pytest
from bs4 import BeautifulSoup

pytest_plugins = ["docker_compose"]
DOCKER_COMPOSE_IMAGE = "web"


@pytest.fixture(scope="module")
def wait_for_frontend(module_scoped_container_getter):
    """Wait for the frontend from the docker-compose image to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    request_session.mount("http://", HTTPAdapter(max_retries=retries))

    service = module_scoped_container_getter.get(DOCKER_COMPOSE_IMAGE).network_info[0]
    port = service.host_port
    base_url = f"http://localhost:{port}/"
    assert request_session.get(base_url)
    return request_session, base_url


@pytest.fixture
def get_response(wait_for_frontend):
    request_session, base_url = wait_for_frontend

    def response_callback(path_url=""):
        concat_url = urljoin(base_url, path_url)
        response = request_session.get(concat_url)
        return response, concat_url

    yield response_callback


@pytest.mark.e2e
def test_index_page_title(get_response):
    # Given
    response, _given_url = get_response("/")

    # When
    soup = BeautifulSoup(response.content, "html.parser")
    tag = soup.select_one("title")

    # Then
    assert tag is not None
    assert "Variant Effect Predictor - VEP WebApp" in tag.text


@pytest.mark.e2e
def test_index_page_content(get_response):
    response, _ = get_response("/")

    assert "Hello world" in str(response.content)


@pytest.mark.e2e
def test_index_page_status(get_response):
    response, _ = get_response("/")

    assert response.status_code == 200
