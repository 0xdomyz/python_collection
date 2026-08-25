# %%
import shutil
from pathlib import Path

from git import Repo

# %%
repo_location = r"C:\Users\yzdom\Projects\test_1"
branches_parent_location = r"C:\Users\yzdom\Projects\test_1_branches"

# %%
# get all branches from a repo
rp = Repo(repo_location)
rp.branches

# %%
# setup target location for 1st time
try:
    if Path(branches_parent_location).exists():
        shutil.rmtree(branches_parent_location)
    Path(branches_parent_location).mkdir(parents=True, exist_ok=True)
    
    # copy paste
    for branch in rp.branches:
        # copy from master repo
        target_location = branches_parent_location + "\\" + branch.name
        print(f"copying from {repo_location} to {target_location}")
        shutil.copytree(repo_location, target_location)
except Exception as e:
    print(f"Please manually delete {branches_parent_location}: {e}")


# %%
for branch in rp.branches:
    target_location = branches_parent_location + "\\" + branch.name
    repo = Repo(target_location)
    print(f"checking out {branch.name}")
    repo.git.checkout(branch.name)

