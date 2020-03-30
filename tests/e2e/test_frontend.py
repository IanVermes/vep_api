import requests
import pytest
from bs4 import BeautifulSoup

pytest_plugins = ["docker_compose"]


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

    assert "VEP Uploader" in str(response.content)


@pytest.mark.e2e
def test_index_page_status(get_response):
    response, _ = get_response("/")

    assert response.status_code == 200
