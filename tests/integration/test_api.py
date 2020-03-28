import pytest


def test_api_POST_ping_RESP_pong_with_valid_data(client):
    # Given
    expected_path = "/api/ping"
    input_json = {"data": "ping"}
    expected_response_json = {"data": "pong"}

    # When
    resp = client.post("/ping", json=input_json)

    # Then
    assert resp.status_code == 201
    assert response.json() == expected_response_json


def test_api_POST_ping_RESP_pong_with_invalid_data(client):
    # Given
    eexpected_path = "/api/ping"
    input_json = {"foo": "bar"}

    # When
    resp = client.post("/ping", json=input_json)

    # Then
    # 400 response status code indicates that the server cannot or will not
    # process the request i.e. Bad Request
    assert resp.status_code == 400
