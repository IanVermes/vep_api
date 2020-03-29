import pytest

from webvep.helpers import vcf_helpers


@pytest.mark.parametrize(
    "string,expected",
    [
        pytest.param("bos_taurus_UMD3.1.vcf", ("bos", "taurus")),
        pytest.param("canis_familiaris_CanFam3.1.vcf", ("canis", "familiaris")),
        pytest.param(
            "drosophila_melanogaster_BDGP6.vcf", ("drosophila", "melanogaster")
        ),
        pytest.param("homo_sapiens_GRCh38.vcf", ("homo", "sapiens")),
        pytest.param("rattus_norvegicus_Rnor_6.0.vcf", ("rattus", "norvegicus")),
    ],
)
def test_extract_binomial_name(string, expected):
    # When
    actual = vcf_helpers.extract_binomial_name(string)

    # Then
    assert actual == expected


def test_validate_vcf_content_with_valid_file(valid_vcf_file):
    # Given
    with open(valid_vcf_file, "r") as handle:

        # When
        result = vcf_helpers.validate_vcf_content(handle)

    # Then
    assert result == True


def test_validate_vcf_content_with_invalid_file(valid_vcf_file, tmp_path):
    # Given
    invalid_file = tmp_path / valid_vcf_file.name  # use a valid name but invalid data
    invalid_file.write_text("# foo" * 100)
    with open(invalid_file, "r") as handle:

        # When
        result = vcf_helpers.validate_vcf_content(handle)

    # Then
    assert result == False


def test_module_constant_BINOMIAL_NAMES():
    assert ("bos", "taurus") in vcf_helpers.BINOMIAL_NAMES
    assert ("homo", "sapiens") in vcf_helpers.BINOMIAL_NAMES
    assert ("foo", "bar") not in vcf_helpers.BINOMIAL_NAMES
