import pathlib

import pytest

from webvep_api.forms import VcfForm
from webvep.helpers import vep_helper


## FIXTURES

VEP_FILE_DATA = b"foobar"
VEP_ERROR_MSG = "stderr error message"


@pytest.fixture
def vcf_form(valid_vcf_file):
    name = valid_vcf_file.name
    data = valid_vcf_file.read_bytes()
    return VcfForm(name, data)


@pytest.fixture
def mock_execute_subprocess_FAILING(monkeypatch):
    def mock_execute_subprocess(cmd):
        return (1, VEP_ERROR_MSG)

    monkeypatch.setattr(
        vep_helper, "execute_subprocess", mock_execute_subprocess, raising=True
    )


@pytest.fixture
def mock_execute_subprocess_PASSING(monkeypatch):
    def mock_execute_subprocess(cmd):
        cmd_string = " ".join(cmd)
        # From the command string extract the output file
        _rest, out_file = cmd_string.rsplit("-o ", maxsplit=1)
        out_file = pathlib.Path(out_file)
        out_file.write_bytes(VEP_FILE_DATA)
        return (0, "")

    monkeypatch.setattr(
        vep_helper, "execute_subprocess", mock_execute_subprocess, raising=True
    )


@pytest.fixture
def mock_processor_in_docker(tmp_path):
    temp_dir = tmp_path / "MOCK_VOLUME"
    temp_dir.mkdir()
    assert temp_dir.exists()
    temp_script_dir = tmp_path / "SCRIPT_DIRECTORY"
    temp_script = temp_script_dir / "vep.pl"
    temp_script_dir.mkdir()
    temp_script.touch()
    assert temp_script.exists()
    processor = vep_helper.ProcessVcfForm()
    processor.IN_DOCKER = True
    processor.VOLUME_PATH = temp_dir
    processor.VEP_SCRIPT_PATH = temp_script
    yield processor


## HELPERS


def count_files_in_dir(path):
    path = pathlib.Path(path)
    file_iterator = (f for f in path.rglob("*") if f.is_file())
    return len(list(file_iterator))


## TESTS


def test_ProcessVcfForm_with_VcfForm_that_passes_script(
    vcf_form, mock_processor_in_docker, mock_execute_subprocess_PASSING
):
    # Given
    processor = mock_processor_in_docker
    files_found_before = count_files_in_dir(processor.VOLUME_PATH)

    # When
    vep_form = processor.pipeline(vcf_form)
    files_found_after = count_files_in_dir(processor.VOLUME_PATH)

    # Then
    assert files_found_before == 0
    assert files_found_after == files_found_before
    assert vep_form.is_valid() == True
    assert vep_form.error == ""
    assert vep_form.raw_data == VEP_FILE_DATA


def test_ProcessVcfForm_with_VcfForm_that_fails_script(
    vcf_form, mock_processor_in_docker, mock_execute_subprocess_FAILING
):
    # Given
    processor = mock_processor_in_docker
    files_found_before = count_files_in_dir(processor.VOLUME_PATH)

    # When
    vep_form = processor.pipeline(vcf_form)
    files_found_after = count_files_in_dir(processor.VOLUME_PATH)

    # Then
    assert files_found_before == 0
    assert files_found_after == files_found_before
    assert vep_form.is_valid() == False
    assert vep_form.error == VEP_ERROR_MSG
    assert vep_form.raw_data == b""


def test_ProcessVcfForm_generate_vep_script_command():
    # Given
    script = pathlib.Path("~/src/ensembl-vep/vep")
    in_file = pathlib.Path("/opt/vep/.vep/input/homo_sapiens_GRCh38.vcf")
    out_file = pathlib.Path("/opt/vep/.vep/output.txt")
    expected_cmd = (
        f"perl {str(script)} --offline --hgvs -i {str(in_file)} -o {str(out_file)}"
    )

    # When
    processor = vep_helper.ProcessVcfForm()
    cmd = processor.generate_vep_script_command(script, in_file, out_file)
    cmd_as_string = " ".join(cmd)

    # Then
    assert expected_cmd == cmd_as_string


def test_ProcessVcfForm_write_to_volume(mock_processor_in_docker):
    # Given
    processor = mock_processor_in_docker
    files_found_before = count_files_in_dir(processor.VOLUME_PATH)
    data = b"bin bat bar"
    name = "example.vcf"

    # When
    new_file = processor.write_to_volume(name, data)
    files_found_after = count_files_in_dir(processor.VOLUME_PATH)

    # Then
    assert new_file.exists()
    assert new_file.read_bytes() == data
    assert files_found_before == 0
    assert files_found_after - files_found_before == 1
