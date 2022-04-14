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

def make_dir_and_2_parents_if_not_exist(path: Path):
    if not path.parents[1].exists():
        path.parents[1].mkdir()
    if not path.parent.exists():
        path.parent.mkdir()
    if not path.exists():
        path.mkdir()

def clone_repo_if_not_exist_on_path(path: Path, repo_name, repo_address):
    if not (path / repo_name).exists():
        with cd(path):
            subprocess.run(f"git clone {repo_address}", shell=True, check=True)

def run_cmd_on_path(cmd, path):
    with cd(path):
        subprocess.run(cmd, shell=True, check=True)

if __name__ == "__main__":
    root_path = (Path(__file__).parents[2] / 'python_shell_example').resolve()
    sub_paths = ['f1/sf1', 'f2/sf2']
    paths = [root_path / sub_path for sub_path in sub_paths]
    repo_name = 'python_collection'
    repo_address = f'git@github.com:0xdomyz/{repo_name}.git'
    for path in paths:
        make_dir_and_2_parents_if_not_exist(path)
        clone_repo_if_not_exist_on_path(path, repo_name, repo_address)
        run_cmd_on_path("git pull origin master", path / repo_name)
        run_cmd_on_path("dir", path)

