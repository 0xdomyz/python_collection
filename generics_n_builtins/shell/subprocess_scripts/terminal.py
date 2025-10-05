import subprocess


def run_shell_cmd(cmd: str) -> str:
    completed_proc = subprocess.run(cmd, shell=True, capture_output=True)
    completed_proc.check_returncode()
    return completed_proc.stdout.decode("utf-8")


from contextlib import contextmanager
import os
from pathlib import Path


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def run_shell_cmd_on_path(cmd: str, path: Path) -> str:
    with cd(path):
        return run_shell_cmd(cmd)
