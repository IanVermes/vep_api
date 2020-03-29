import pytest

from webvep.helpers import vep_helper


def test_ProcessVcfForm_raises_runtime_error_outside_docker():
    # Given
    processor = vep_helper.ProcessVcfForm()

    # Then
    if processor.IN_DOCKER:
        pass
    else:
        with pytest.raises(RuntimeError):
            processor.docker_check()


@pytest.mark.docker
def test_ProcessVcfForm_executes_without_error_inside_docker_when_docker_checking():
    # Given
    processor = vep_helper.ProcessVcfForm()

    # When
    result = processor.docker_check()  # the method should return nothing if successful

    # Then
    assert result is None


@pytest.mark.docker
def test_ProcessVcfForm_executes_without_error_inside_docker_when_env_checking():
    # Given
    processor = vep_helper.ProcessVcfForm()

    # When
    result = processor.env_check()  # the method should return nothing if successful

    # Then
    assert result is None


@pytest.mark.docker
def test_ProcessVcfForm_tester_cmd_checks_vep_script_works():
    # Given
    processor = vep_helper.ProcessVcfForm()
    processor.env_check()

    # When
    cmd = processor.generate_vep_test_command(processor.VEP_SCRIPT_PATH)
    outcome, err_msg = vep_helper.execute_subprocess(cmd)

    # Then
    assert outcome == 0
    assert err_msg == ""
