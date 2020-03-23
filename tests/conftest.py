import typing as t

import pytest
from django.core.files import File


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
    yield file


@pytest.fixture(scope="session")
def vcf_django_file(vcf_file):
    # The models.Model built-in field `FileField` takes Django File objects and not
    # pathlib.Path or str objects
    django_file = File(open(vcf_file, "rb"))
    yield django_file


@pytest.fixture(scope="session")
def vcf_django_file_and_expected_name(vcf_django_file):
    yield (vcf_django_file, VCF_FILE_NAME)


@pytest.fixture()
def mock_MEDIA_ROOT(monkeypatch, tmp_path_factory):
    from django.conf import settings

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


## Marks


# Hooks for the mark @pytest.mark.incremental with logic copied from
# https://docs.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps

# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: t.Dict[str, t.Dict[t.Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))
