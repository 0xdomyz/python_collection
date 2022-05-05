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


def make_dirs_if_not_exist(path: Path, number_of_parents: int = 2):
    """
    Examples
    -----------
    >>> make_dirs_if_not_exist(Path('.') / 'test' / 'test' / 'test')
    >>> make_dirs_if_not_exist(Path('.') / 'test' / 'test' / 'test' / 'test')
    FileNotFoundError: [WinError 3] ...
    """
    for i in reversed(range(number_of_parents)):
        if not path.parents[i].exists():
            path.parents[i].mkdir()
    if not path.exists():
        path.mkdir()


if __name__ == "__main__":
    root_path = (Path(__file__).parents[2] / "python_shell_example").resolve()
    sub_paths = ["f1/sf1", "f2/sf2"]
    paths = [root_path / sub_path for sub_path in sub_paths]
    repo_name = "python_collection"
    repo_address = f"git@github.com:0xdomyz/{repo_name}.git"
    for path in paths:
        print(f"on path: {path.as_posix()}")
        make_dirs_if_not_exist(path)
        if not (path / repo_name).exists():
            run_cmd_on_path(f"git clone {repo_address}", path)
        run_cmd_on_path("git pull origin master", path / repo_name)
        run_cmd_on_path("dir", path)
