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


def test_api_POST_vcf_file_RESP_formatted_json_with_valid_file(client, valid_vcf_file):
    # Given
    expected_path = "/api/vcf/"
    expected_response_json = {"is_valid": True}
    with open(valid_vcf_file, "rb") as handle:
        input_data = {"vcf_file": handle}

        # When
        response = client.post(expected_path, input_data)

    # Then
    assert response.status_code == 201
    assert response.json() == expected_response_json


def test_api_POST_vcf_file_RESP_formatted_json_with_invalid_file(
    client, invalid_vcf_file
):
    # Given
    expected_path = "/api/vcf/"
    expected_response_json = {"is_valid": False}
    with open(invalid_vcf_file, "rb") as handle:
        input_data = {"vcf_file": handle}

        # When
        response = client.post(expected_path, input_data)

    # Then
    assert response.status_code == 400
    assert response.json() == expected_response_json


# def test_api_POST_vep_RESP_formatted_vep_data_with_valid_file(
#     client, valid_vcf_file
# ):
#     # Given
#     expected_path = "/api/vep/"
#     expected_response_json_keys = ["VEP-version", "run-date", "results"]
#     with open(valid_vcf_file, "rb") as handle:
#         input_data = {"vcf_file": handle}

#         # When
#         response = client.post(expected_path, input_data)
#         result_json = response.json()

#     # Then
#     assert response.status_code == 201
#     for key in expected_response_json_keys:
#         assert key in result_json


# def test_api_POST_vep_RESP_formatted_vep_data_with_invalid_file(
#     client, invalid_vcf_file
# ):
#     # Given
#     expected_path = "/api/vep/"
#     expected_response_json = {"is_valid": False}
#     with open(invalid_vcf_file, "rb") as handle:
#         input_data = {"vcf_file": handle}

#         # When
#         response = client.post(expected_path, input_data)

#     # Then
#     assert response.status_code == 400
#     assert response.json() == expected_response_json
