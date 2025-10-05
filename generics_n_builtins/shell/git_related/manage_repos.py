"""
Manage Repos
^^^^^^^^^^^^^^^^

Examples
----------
Usage as cli::

    python manage_repos.py -h

Funcs are also usable as python func.

"""

import os
import subprocess
from argparse import ArgumentParser
from contextlib import contextmanager
from pathlib import Path

path = Path(__file__).parent
parser = ArgumentParser()
parser.add_argument(
    "-f", "--function", help="Use function, possible ones: pull_all, make_html_all"
)
parser.add_argument("-c", "--command", help="Run commands, e.g.: git status")


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


def pull_all():
    for dir in path.iterdir():
        if dir.is_dir():
            if (dir / ".git").exists():
                print(f"on: {dir.resolve()}")
                print("-" * 80)
                run_cmd_on_path("git pull", dir)
                print("\n" * 2)


def run_cmds(cmd: str):
    for dir in path.iterdir():
        if dir.is_dir():
            if (dir / ".git").exists():
                print(f"on: {dir.resolve()}")
                print("-" * 80)
                run_cmd_on_path(cmd, dir)
                print("\n" * 2)


def make_html_all():
    for dir in path.iterdir():
        if dir.is_dir():
            sphinx_build_files = [
                dir / "docs",
                dir / "docs" / "Makefile",
                dir / "docs" / "make.bat",
            ]

            if all(file.exists() for file in sphinx_build_files):
                print(f"on: {dir.resolve()}")
                print("-" * 80)
                run_cmd_on_path("make html", dir / "docs")
                print("\n" * 2)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.function is not None:
        eval(f"{args.function}()")
    elif args.command is not None:
        run_cmds(args.command)
    else:
        pull_all()
