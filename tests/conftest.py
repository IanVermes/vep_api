import pathlib

import pytest

## FIXTURES


@pytest.fixture
def valid_vcf_file():
    filepath = pathlib.Path("tests/resources/homo_sapiens_GRCh38.vcf")
    if not filepath.exists():
        raise FileNotFoundError(filepath)
    else:
        return filepath


@pytest.fixture
def invalid_vcf_file():
    filepath = pathlib.Path("tests/resources/badly_named.vcf")
    if not filepath.exists():
        raise FileNotFoundError(filepath)
    else:
        return filepath


## PYTEST SETUP


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-e2e"):
        # --run-e2e given in cli: do not skip e2e tests
        return
    skip_slow = pytest.mark.skip(
        reason=(
            "tests should not be called within a "
            "docker image: need --run-e2e option to run "
        )
    )
    skip_in_docker = pytest.mark.skip(
        reason=(
            "tests tests should not be called outside a "
            "docker image: need --run-in-docker option to run "
        )
    )
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_slow)
        elif "docker" in item.keywords:
            item.add_marker(skip_in_docker)


def pytest_addoption(parser):
    parser.addoption(
        "--run-e2e", action="store_true", default=False, help="run end2end tests"
    )
    parser.addoption(
        "--run-in-docker",
        action="store_true",
        default=False,
        help="run tests that should only work in docker",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        (
            "e2e: mark end2end test -- supposed to be run outside of a Docker/Docker "
            "compose instance"
        ),
    )
    config.addinivalue_line(
        "markers",
        (
            "docker: mark docker test -- supposed to be run inside of a Docker/Docker "
            "compose instance"
        ),
    )
