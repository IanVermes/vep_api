import json

import pytest


def test_api_POST_ping_RESP_pong_with_valid_data(client):
    # Given
    expected_path = "/api/ping/"
    input_json = {"data": "ping"}
    expected_response_json = {"data": "pong"}

    # When
    response = client.post(expected_path, input_json)

    # Then
    assert response.status_code == 201
    assert response.json() == expected_response_json


def test_api_POST_ping_RESP_pong_with_invalid_data(client):
    # Given
    expected_path = "/api/ping/"
    input_json = {"foo": "bar"}

    # When
    response = client.post(expected_path, input_json)

    # Then
    # 400 response status code indicates that the server cannot or will not
    # process the request i.e. Bad Request
    assert response.status_code == 400
