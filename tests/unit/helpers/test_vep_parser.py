import pytest

from webvep.helpers import vep_parser


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        pytest.param("21:25592836", ("21", "25592836", "")),
        pytest.param("21:25592860", ("21", "25592860", "")),
        pytest.param("21:25603832-25603999", ("21", "25603832", "25603999")),
        pytest.param("-", ("", "", "")),
    ],
)
def test_parse_location(input_value, expected_value):
    # When
    actual_value = vep_parser.parse_location(input_value)

    # Then
    assert actual_value == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        pytest.param("ENSG00000181123", "ENSG00000181123"),
        pytest.param("ENSG00000182541", "ENSG00000182541"),
        pytest.param("ENSG00000182670", "ENSG00000182670"),
        pytest.param("-", ""),
    ],
)
def test_parse_gene(input_value, expected_value):
    # When
    actual_value = vep_parser.parse_gene(input_value)

    # Then
    assert actual_value == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        pytest.param("ENST00000215812", "ENST00000215812"),
        pytest.param("ENST00000216027", "ENST00000216027"),
        pytest.param("ENST00000262607", "ENST00000262607"),
        pytest.param("-", ""),
    ],
)
def test_parse_transcript(input_value, expected_value):
    # When
    actual_value = vep_parser.parse_transcript(input_value)

    # Then
    assert actual_value == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        pytest.param("Transcript", "Transcript"),
        pytest.param("RegulatoryFeature", "Regulatory Feature"),
        pytest.param("MotifFeature", "Motif Feature"),
        pytest.param("-", ""),
    ],
)
def test_parse_transcript_type(input_value, expected_value):
    # When
    actual_value = vep_parser.parse_transcript_type(input_value)

    # Then
    assert actual_value == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        pytest.param("5_prime_UTR_variant", ("5_prime_UTR_variant",)),
        pytest.param("downstream_gene_variant", ("downstream_gene_variant",)),
        pytest.param(
            "5_prime_UTR_variant,NMD_transcript_variant",
            ("5_prime_UTR_variant", "NMD_transcript_variant"),
        ),
        pytest.param(
            "incomplete_terminal_codon_variant,coding_sequence_variant",
            ("incomplete_terminal_codon_variant", "coding_sequence_variant"),
        ),
        pytest.param(
            "splice_region_variant,3_prime_UTR_variant,NMD_transcript_variant",
            ("splice_region_variant", "3_prime_UTR_variant", "NMD_transcript_variant"),
        ),
        pytest.param("-", tuple()),
    ],
)
def test_parse_consequence_type(input_value, expected_value):
    # When
    actual_value = vep_parser.parse_consequence(input_value)

    # Then
    assert actual_value == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        pytest.param(
            "IMPACT=LOW;STRAND=-1;HGVSc=ENST00000262607.3:c.1359T>C;HGVSp=ENSP00000262607.2:p.Tyr453%3D",
            "ENST00000262607.3:c.1359T>C",
        ),
        pytest.param("IMPACT=MODIFIER;DISTANCE=1368;STRAND=-1", ""),
        pytest.param(
            "IMPACT=LOW;STRAND=-1;HGVSc=ENST00000263207.8:c.1290C>T;HGVSp=ENSP00000263207.3:p.Gly430%3D",
            "ENST00000263207.8:c.1290C>T",
        ),
        pytest.param("-", ""),
    ],
)
def test_parse_hgvsc(input_value, expected_value):
    # When
    actual_value = vep_parser.parse_hgvsc(input_value)

    # Then
    assert actual_value == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        pytest.param(
            "IMPACT=LOW;STRAND=-1;HGVSc=ENST00000262607.3:c.1359T>C;HGVSp=ENSP00000262607.2:p.Tyr453%3D",
            "ENSP00000262607.2:p.Tyr453%3D",
        ),
        pytest.param("IMPACT=MODIFIER;DISTANCE=1368;STRAND=-1", ""),
        pytest.param(
            "IMPACT=LOW;STRAND=-1;HGVSc=ENST00000263207.8:c.1290C>T;HGVSp=ENSP00000263207.3:p.Gly430%3D",
            "HGVSp=ENSP00000263207.3:p.Gly430%3D",
        ),
        pytest.param("-", ""),
    ],
)
def test_parse_hgvsp(input_value, expected_value):
    # When
    actual_value = vep_parser.parse_hgvsp(input_value)

    # Then
    assert actual_value == expected_value
