"""This module wraps the dockerised perl VEP program & process VcfForms into VepForms"""
import uuid
import os
import subprocess
import shlex
import pathlib
import shutil

import typing as t

from webvep_api.forms import VepForm

if t.TYPE_CHECKING:
    from webvep_api.forms import VcfForm


class ProcessVcfForm:
    """Wrap the VEP program, piping vcf data in, piping vep result & maintain a clean filesystem"""

    def __init__(self):
        self.IN_DOCKER = bool(os.getenv("IN_DOCKER", 0))
        self.VEP_SCRIPT_PATH = os.getenv("VEP_SCRIPT_PATH", ".")
        self.VOLUME_PATH = os.getenv("VOLUME_PATH", "")
        self.UNFORMATTED_PERL_COMMAND = (
            "perl {script} --offline --hgvs  -i {in_file} -o {out_file}"
        )
        self._check = False

    def docker_check(self):
        if not self.IN_DOCKER:
            raise RuntimeError(
                "Cannot perform this operation unless in a Docker container."
            )
        self._check = True

    def env_check(self):
        if not self.VEP_SCRIPT_PATH:
            raise RuntimeError(
                "Cannot perform this operation as VEP_SCRIPT_PATH was not set in the environment"
            )
        else:
            self.VEP_SCRIPT_PATH = pathlib.Path(self.VEP_SCRIPT_PATH).expanduser()
        if not self.VOLUME_PATH:
            raise RuntimeError(
                "Cannot perform this operation as VOLUME_PATH was not set in the environment"
            )
        else:
            self.VOLUME_PATH = pathlib.Path(self.VOLUME_PATH)
        self._check = True

    def pipeline(self, vcf_form: "VcfForm") -> VepForm:
        """Process a Vcf representation with the VEP script and return the output."""
        if not self._check:
            self.docker_check()
            self.env_check()
        out_file = self.generate_outfile()
        in_file = self.write_to_volume(vcf_form.filename, vcf_form.content)
        command = self.generate_vep_script_command(
            self.VEP_SCRIPT_PATH, in_file, out_file
        )
        try:
            outcome, err_msg = execute_subprocess(command)
            if outcome == 0:
                out_data: bytes = out_file.read_bytes()
            else:
                out_data = b""
        finally:
            # Tidy up input/output files after script execution
            if in_file.exists():
                in_file.unlink()
            if in_file.parent.exists():
                in_file.parent.rmdir()
            if out_file.exists():
                out_file.unlink()
            if out_file.parent.exists():
                shutil.rmtree(out_file.parent)

        return VepForm(raw_data=out_data, error=err_msg)

    def _create_unique_volume_filename(self, filename: str) -> pathlib.Path:
        volume = self.VOLUME_PATH
        temp_dir = (
            volume / str(uuid.uuid4())[:13]
        )  # 13 digits of the uuid looks like `cd3d327e-9037`
        temp_dir.mkdir()
        volume_file = temp_dir / filename
        return volume_file

    def write_to_volume(self, filename: str, content: bytes) -> pathlib.Path:
        volume_file = self._create_unique_volume_filename(filename)
        volume_file.write_bytes(content)
        return volume_file

    def generate_outfile(self) -> pathlib.Path:
        volume_file = self._create_unique_volume_filename("variant_effect_output.txt")
        return volume_file

    def generate_vep_script_command(
        self, script: pathlib.Path, in_file: pathlib.Path, out_file: pathlib.Path
    ) -> t.List[str]:
        cmd = self.UNFORMATTED_PERL_COMMAND.format(
            script=shlex.quote(str(script)),
            in_file=shlex.quote(str(in_file)),
            out_file=shlex.quote(str(out_file)),
        )
        split_cmd = shlex.split(cmd)
        return split_cmd

    def generate_vep_test_command(self, script: pathlib.Path) -> t.List[str]:
        cmd = "perl {script}".format(script=shlex.quote(str(script)))
        split_cmd = shlex.split(cmd)
        return split_cmd


def execute_subprocess(cmd: t.List[str]) -> t.Tuple[int, str]:
    """Run a subprocess from a formatted command and return the status code err msg"""
    completed_process = subprocess.run(
        cmd, timeout=30, capture_output=True, encoding="utf8"
    )
    if completed_process.returncode:
        print(f"{cmd=}")
        print(f"{completed_process.returncode=}")
        print(f"{completed_process.stdout=}")
        print(f"{completed_process.stderr=}")
    return (completed_process.returncode, completed_process.stderr)
