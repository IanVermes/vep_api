import os
import pathlib

import pytest


def test_mock_MEDIA_ROOT(mock_MEDIA_ROOT):
    from django.conf import settings

    path = settings.MEDIA_ROOT

    assert os.path.exists(path)
    assert "mock_MEDIA_ROOT" in path


def test_vcf_django_file_fixture(vcf_django_file):
    path = pathlib.Path(vcf_django_file.name)
    assert path.exists()
    assert path.name == "bos_taurus_UMD3.1.vcf"
