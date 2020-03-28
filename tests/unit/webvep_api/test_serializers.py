import pytest

from webvep_api.serializers import PingSerializer


def test_Ping_serializer_validates():
    # Given
    valid_data = {"data": "ping"}

    # When
    serlializer = PingSerializer(data=valid_data)

    # Then
    assert serlializer.is_valid()


@pytest.mark.parametrize(
    "invalid_data",
    [
        pytest.param({"foo": "ping"}, id="wrong field", marks=pytest.mark.xfail),
        pytest.param({"data": "pong"}, id="wrong value", marks=pytest.mark.xfail),
        pytest.param({}, id="empty data", marks=pytest.mark.xfail),
    ],
)
def test_Ping_serializer_invalidates_bad_data(invalid_data):
    # When
    serlializer = PingSerializer(data=invalid_data)

    # Then
    assert serlializer.is_valid()
