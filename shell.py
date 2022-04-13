import shutil
import os
from pathlib import Path

def start(path):
    os.startfile(path)

import subprocess
repo_name = 'python_collection'
repo_address = f'git@github.com:0xdomyz/{repo_name}.git'
subprocess.run(["git", "clone", repo_address])
subprocess.run(["cd", repo_name])
subprocess.run(["git", "pull"])
subprocess.run(["cd", '..'])
