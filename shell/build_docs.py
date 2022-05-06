import subprocess
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


def run_cmd_on_path(cmd: str, path: Path) -> subprocess.CompletedProcess[str]:
    with cd(path):
        print(f"{path.resolve()}/{cmd}")
        return subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    path = Path(__file__).parent

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
