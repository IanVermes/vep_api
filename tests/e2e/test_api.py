from urllib.parse import urljoin

import pytest

pytest_plugins = ["docker_compose"]

API_ROOT = "/api/"


@pytest.fixture
def post_json_get_response(wait_for_docker_to_load):
    request_session, base_url = wait_for_docker_to_load
    api_url = urljoin(base_url, API_ROOT)

    def response_callback(path_url="", json={}):
        concat_url = urljoin(base_url, path_url)
        response = request_session.post(concat_url, json=json)
        return response, concat_url

    yield response_callback


@pytest.mark.e2e
def test_api_POST_ping_RESP_pong_with_valid_data(post_json_get_response):
    # Given
    expected_path = "/api/ping"
    input_json = {"data": "ping"}
    expected_response_json = {"data": "pong"}

    # When
    resp, called_url = post_json_get_response("/ping", input_json)

    # Then
    assert called_url.enswith(expected_path)
    assert resp.status_code == 201
    assert response.json() == expected_response_json


@pytest.mark.e2e
def test_api_POST_ping_RESP_pong_with_invalid_data(post_json_get_response):
    # Given
    expected_path = "/api/ping"
    input_json = {"foo": "bar"}

    # When
    resp, called_url = post_json_get_response("/ping", input_json)

    # Then
    assert called_url.enswith(expected_path)
    # 400 response status code indicates that the server cannot or will not
    # process the request i.e. Bad Request
    assert resp.status_code == 400
