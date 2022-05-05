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
        return subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    path = Path(__file__).parent
    for dir in path.iterdir():
        if dir.is_dir():
            if (dir / ".gitignore").exists():
                print(f"on: {dir.resolve()}")
                print("-"*80)
                try:
                    run_cmd_on_path("git pull origin master", dir)
                except Exception as ex:
                    run_cmd_on_path("git pull origin main", dir)
                print("")
                print("")
