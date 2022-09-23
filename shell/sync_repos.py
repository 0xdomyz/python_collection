"""
Sync all repos in folder.

Examples
----------
Usage as cli::

    python sync_repos.py

Usage in python::

    import sync_repos
    sync_repos.main()
"""

import subprocess
from contextlib import contextmanager
import os
from pathlib import Path

path = Path(__file__).parent

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

def main():
    for dir in path.iterdir():
        if dir.is_dir():
            if (dir / ".gitignore").exists():
                print(f"on: {dir.resolve()}")
                print("-"*80)

                run_cmd_on_path("git pull", dir)
                
                print("")
                print("")


if __name__ == "__main__":
    main()
