import pytest

from webvep_api.forms import VcfForm
from webvep.helpers import vep_helper


@pytest.mark.docker_after_build
def test_ProcessVcfForm_pipeline(valid_vcf_file):
    # Given
    vcf_form = VcfForm(
        filename=valid_vcf_file.name, content=valid_vcf_file.read_bytes()
    )
    processor = vep_helper.ProcessVcfForm()

    # When
    vep_form = processor.pipeline(vcf_form)

    # Then
    assert vep_form.is_valid()
