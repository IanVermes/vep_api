import os
import pathlib
import shutil

import pytest
from django.conf import settings

from vcfupload.models import UploadVcf

## Tests


@pytest.mark.django_db
def test_uploadvcf_create(vcf_django_file, mock_MEDIA_ROOT):
    # Given
    before_db_count = len(UploadVcf.objects.all())

    # When
    _upload_vcf = UploadVcf.objects.create(file=vcf_django_file)
    after_db_count = len(UploadVcf.objects.all())

    # Then
    assert before_db_count == 0
    assert after_db_count - before_db_count == 1


@pytest.mark.django_db
def test_uploadvcf_create_writes_file_to_MEDIA_ROOT(vcf_django_file, mock_MEDIA_ROOT):
    # Given
    media_root_path = pathlib.Path(settings.MEDIA_ROOT)
    before_filesys_count = len(list(media_root_path.glob("*.*")))

    # When
    _upload_vcf = UploadVcf.objects.create(file=vcf_django_file)
    after_filesys_count = len(list(media_root_path.glob("*.*")))

    # Then
    assert before_filesys_count == 0
    assert after_filesys_count - before_filesys_count == 1


@pytest.mark.django_db
def test_uploadvcf_create_sets_original_filename(
    vcf_django_file_and_expected_name, mock_MEDIA_ROOT
):
    # Given
    vcf_django_file, expected_name = vcf_django_file_and_expected_name

    # When
    upload_vcf = UploadVcf.objects.create(file=vcf_django_file)

    # Then
    assert upload_vcf.original_filename == expected_name


@pytest.mark.django_db
def test_uploadvcf_create_sets_file(vcf_django_file, mock_MEDIA_ROOT):
    # Given
    expected_prefix = pathlib.Path(vcf_django_file.name).suffix

    # When
    upload_vcf = UploadVcf.objects.create(file=vcf_django_file)
    actual_suffix = pathlib.Path(upload_vcf.file.name).suffix

    # Then
    assert upload_vcf.original_filename != upload_vcf.file.name
    assert expected_prefix == actual_suffix
