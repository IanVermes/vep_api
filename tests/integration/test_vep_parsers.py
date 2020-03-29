import pytest

from webvep.webvep_api.forms import VepForm
from webvep.helpers import vep_parser

VEP_RAW_OUTPUT_COLUMNS = (
    "Uploaded_variation",
    "Location",
    "Allele",
    "Gene",
    "Feature",
    "Feature_type",
    "Consequence",
    "cDNA_position",
    "CDS_position",
    "Protein_position",
    "Amino_acids",
    "Codons",
    "Existing_variation",
    "Extra",
)


@pytest.fixture(scope="module")
def vep_form(vep_output_file):
    result = VepForm(raw_data=vep_output_file.read_bytes(), error="")
    assert result.is_valid()
    yield result


def test_raw_parser_output_has_columns_titles(vep_form):
    # Given
    expected = VEP_RAW_OUTPUT_COLUMNS

    # When
    result = vep_parser.raw_parser(vep_form.raw_data)

    # Then
    assert result.columns_names == expected


def test_raw_parser_output_has_correct_number_of_rows(vep_form):
    # Given
    ## Magic value comes from the number of rows in `tests/resources/vep_output_file.txt`
    expected_count = 1345
    first_row = ()

    # When
    result = vep_parser.raw_parser(vep_form.raw_data)

    # Then
    assert len(result.rows) == expected_count


def test_raw_parser_output_has_correct_first_row(vep_form):
    # Given
    first_row = (
        "rs7289170",
        "22:17181903",
        "G",
        "ENSG00000093072",
        "ENST00000262607",
        "Transcript",
        "synonymous_variant",
        "1571",
        "1359",
        "453",
        "Y",
        "taT/taC",
        "-",
        "IMPACT=LOW;STRAND=-1",
    )

    # When
    result = vep_parser.raw_parser(vep_form.raw_data)

    # Then
    assert result.rows[0] == first_row


def test_raw_parser_output_has_correct_last_row(vep_form):
    # Given
    last_row = (
        "rs5771206",
        "22:50178377",
        "G",
        "ENSG00000073150",
        "ENST00000402472",
        "Transcript",
        "3_prime_UTR_variant,NMD_transcript_variant",
        "1686",
        "-",
        "-",
        "-",
        "-",
        "-",
        "IMPACT=MODIFIER;STRAND=1;FLAGS=cds_start_NF",
    )

    # When
    result = vep_parser.raw_parser(vep_form.raw_data)

    # Then
    assert result.rows[-1] == last_row


def test_raw_parser_output_has_correct_number_of_columns_per_row(vep_form):
    # Given
    ## Magic value comes from the number of rows in `tests/resources/vep_output_file.txt`
    expected_count = len(VEP_RAW_OUTPUT_COLUMNS)

    # When
    result = vep_parser.raw_parser(vep_form.raw_data)

    # Then
    ## `42` corresponds to the line number of the first row `tests/resources/vep_output_file.txt`
    for i, row in enumerate(result.rows, start=42):
        assert expected_count == len(row), f"row={i}"


def test_raw_parser_output_has_expected_meta_data(vep_form):
    # Given
    expected_meta_data_1 = "ENSEMBL VARIANT EFFECT PREDICTOR v99.2"
    expected_meta_data_2 = "Output produced at 2020-03-29 05:10:39"

    # When
    result = vep_parser.raw_parser(vep_form.raw_data)

    # Then
    assert expected_meta_data_1 in result.meta_data
    assert expected_meta_data_2 in result.meta_data
