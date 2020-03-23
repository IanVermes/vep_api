import os
import pathlib
import shutil

import pytest
from django.core.files import File
from django.conf import settings

from vcfupload.models import UploadVcf

## Fixtures

VCF_FILE_NAME = "bos_taurus_UMD3.1.vcf"


@pytest.fixture(scope="session")
def vcf_file(tmp_path_factory):
    content = (
        b"##fileformat=VCFv4.0\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n1"
        b"\t351791\t.\tC\tT\t.\t.\t.\n2\t238166\t.\tT\tC\t.\t.\t.\n3\t204072\t."
        b"\tGT\tG\t.\t.\t.\n"
    )
    temp = tmp_path_factory.mktemp("input")
    file = temp / VCF_FILE_NAME
    file.write_bytes(content)
    # The models.Model built-in field `FileField` takes Django File objects and not
    # pathlib.Path or str objects
    django_file = File(open(file, "rb"))
    yield django_file


@pytest.fixture()
def mock_MEDIA_ROOT(monkeypatch, tmp_path_factory):
    base_temp = tmp_path_factory.getbasetemp()
    temp_dir = base_temp / "mock_MEDIA_ROOT"
    monkeypatch.setattr(settings, "MEDIA_ROOT", str(temp_dir))

    yield

    # Clean temp directory between fixture calls
    for tmpfile in temp_dir.iterdir():
        if tmpfile.is_file():
            tmpfile.unlink()
        else:
            shutil.rmtree(tmpfile)
    return


## Fixture tests


def test_mock_MEDIA_ROOT(mock_MEDIA_ROOT):
    from django.conf import settings

    path = settings.MEDIA_ROOT

    assert os.path.exists(path)
    assert "mock_MEDIA_ROOT" in path


def test_vcf_file_fixture(vcf_file):
    path = pathlib.Path(vcf_file.name)
    assert path.exists()
    assert path.name == "bos_taurus_UMD3.1.vcf"


## Tests


@pytest.mark.django_db
def test_uploadvcf_create(vcf_file, mock_MEDIA_ROOT):
    # Given
    before_db_count = len(UploadVcf.objects.all())

    # When
    _upload_vcf = UploadVcf.objects.create(file=vcf_file)
    after_db_count = len(UploadVcf.objects.all())

    # Then
    assert before_db_count == 0
    assert after_db_count - before_db_count == 1


@pytest.mark.django_db
def test_uploadvcf_create_writes_file_to_MEDIA_ROOT(vcf_file, mock_MEDIA_ROOT):
    # Given
    media_root_path = pathlib.Path(settings.MEDIA_ROOT)
    before_filesys_count = len(list(media_root_path.glob("*.*")))

    # When
    _upload_vcf = UploadVcf.objects.create(file=vcf_file)
    after_filesys_count = len(list(media_root_path.glob("*.*")))

    # Then
    assert before_filesys_count == 0
    assert after_filesys_count - before_filesys_count == 1


@pytest.mark.django_db
def test_uploadvcf_create_sets_original_filename(vcf_file, mock_MEDIA_ROOT):
    # When
    upload_vcf = UploadVcf.objects.create(file=vcf_file)

    # Then
    assert upload_vcf.original_filename == VCF_FILE_NAME


@pytest.mark.django_db
def test_uploadvcf_create_sets_file(vcf_file, mock_MEDIA_ROOT):
    # Given
    expected_prefix = pathlib.Path(vcf_file.name).suffix

    # When
    upload_vcf = UploadVcf.objects.create(file=vcf_file)
    actual_suffix = pathlib.Path(upload_vcf.file.name).suffix

    # Then
    assert upload_vcf.original_filename != upload_vcf.file.name
    assert expected_prefix == actual_suffix
