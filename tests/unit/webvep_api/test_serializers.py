import pytest
from django.core.files import File

from webvep_api.serializers import PingSerializer, VcfSerializer


def test_PingSerializer_validates():
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
def test_PingSerializer_invalidates_bad_data(invalid_data):
    # When
    serlializer = PingSerializer(data=invalid_data)

    # Then
    assert serlializer.is_valid()


def test_VcfSerializer_validates_valid_files(valid_vcf_file):
    # Given
    with open(valid_vcf_file, "rb") as handle:
        django_file = File(handle, name=valid_vcf_file.name)
    data = {"vcf_file": django_file}

    # When
    serlializer = VcfSerializer(data=data)

    # Then
    assert serlializer.is_valid()


def test_VcfSerializer_invalidates_bad_filename(invalid_vcf_file):
    # Given
    with open(invalid_vcf_file, "rb") as handle:
        django_file = File(handle, name=invalid_vcf_file.name)
    data = {"vcf_file": django_file}

    # When
    serlializer = VcfSerializer(data=data)

    # Then
    assert not serlializer.is_valid()
