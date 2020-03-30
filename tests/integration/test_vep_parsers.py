import pytest
import datetime
import json

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


def test_ParsedResult_factory_method(vep_form):
    # Given
    raw = vep_parser.raw_parser(vep_form.raw_data)
    expected_variant_count = len(raw.rows)

    # When
    parsed_result = vep_parser.ParsedResult.from_raw(raw)

    # Then
    assert parsed_result.vep_version == "v99.2"
    assert datetime.datetime.strptime(parsed_result.run_date, "%Y-%m-%d %H:%M:%S")
    assert len(parsed_result.variants) == expected_variant_count


def test_ParsedResult_to_json_method(vep_form):
    # Given
    raw = vep_parser.raw_parser(vep_form.raw_data)
    parsed_result = vep_parser.ParsedResult.from_raw(raw)
    json_variants = (v.to_json() for v in parsed_result.variants)
    expected_json = json.dumps(
        json.loads(
            """{{ "VEP-version": "v99.2", "run-date": "{date}", "results": {variants} }}""".format(
                date=parsed_result.run_date, variants=json.dumps(list(json_variants))
            )
        ),
        sort_keys=True,
    )

    # When
    actual_json = json.dumps(parsed_result.to_json(), sort_keys=True)

    # Then
    assert actual_json == expected_json


def test_ParsedVariant_factory_method(vep_form):
    # Given
    raw = vep_parser.raw_parser(vep_form.raw_data)

    # When
    parsed_rows = vep_parser.ParsedVariant.from_raw(raw)
    parsed_row = next(iter(parsed_rows))

    # Then
    assert parsed_row.chromosome == "22"
    assert parsed_row.start == "17181903"
    assert parsed_row.end == ""
    assert parsed_row.gene == "ENSG00000093072"
    assert parsed_row.transcript == "ENST00000262607"
    assert parsed_row.transcript_type == "Transcript"
    assert parsed_row.consequence == "synonymous variant"
    assert parsed_row.hgvsc == "ENST00000262607.3:c.1359T>C"
    assert parsed_row.hgvsp == "ENSP00000262607.2:p.Tyr453%3D"


def test_ParsedVariant_to_json_method(vep_form):
    # Given
    raw = vep_parser.raw_parser(vep_form.raw_data)
    parsed_rows = vep_parser.ParsedVariant.from_raw(raw)
    parsed_row = next(iter(parsed_rows))
    expected_json = json.dumps(
        json.loads(
            """{
                "location": {"chromosome": "22", "start": "17181903", "end": ""},
                "gene": "ENSG00000093072",
                "transcript": "ENST00000262607",
                "feature-type": "Transcript",
                "consequence": ["synonymous variant"],
                "hgvsc": "ENST00000262607.3:c.1359T>C",
                "hgvsp": "ENSP00000262607.2:p.Tyr453%3D"
            }
            """
        ),
        sort_keys=True,
    )

    # When
    actual_json = json.dumps(parsed_row.to_json(), sort_keys=True)

    # Then
    assert actual_json == expected_json


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
        "IMPACT=LOW;STRAND=-1;HGVSc=ENST00000262607.3:c.1359T>C;HGVSp=ENSP00000262607.2:p.Tyr453%3D",
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
        "IMPACT=MODIFIER;STRAND=1;FLAGS=cds_start_NF;HGVSc=ENST00000402472.2:c.*1452A>G",
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
