"""
from terminal import cd, run_cmd_on_path, run

with cd("/home/user"):
    run("ls")

from pathlib import Path
run_cmd_on_path("ls", Path("/home/"))
"""

import os
import subprocess
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def run_cmd_on_path(cmd: str, path: Path) -> subprocess.CompletedProcess[str]:
    with cd(path):
        return subprocess.run(cmd, shell=True, check=True)


def run(cmd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, shell=True, check=True)
