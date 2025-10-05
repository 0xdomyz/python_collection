from git import Repo
import os
from pathlib import Path

# clone down a repo to a location
##################################


def clone_down_repo(repo_ssh, target_parent_location):
    repo_name = repo_ssh.split("/")[-1][:-4]
    target_parent_location = os.path.join(target_parent_location, repo_name)
    Repo.clone_from(repo_ssh, target_parent_location)


repo_ssh = "git@github.com:0xdomyz/utube_playlist_mp3_downloader.git"
target_parent_location = r"C:\Users\yzdom\Projects"
clone_down_repo(repo_ssh=repo_ssh, target_parent_location=target_parent_location)

# get all releases of a repo
############################

repo_loaction = r"C:\Users\yzdom\Projects\utube_playlist_mp3_downloader"


def get_all_releases(repo_loaction):
    repo = Repo(repo_loaction)
    releases = repo.tags
    return releases


releases = get_all_releases(repo_loaction)
releases

# making audit trail of all releases
#############################################################################

# for each tag, clone down the repo to a location, denoted by the tag name
# then checkout the tag


def clone_down_tags(repo_ssh, repo_location, snapshots_parent_location):
    Path(snapshots_parent_location).mkdir(parents=True, exist_ok=True)
    releases = get_all_releases(repo_location)
    for release in releases:
        snapshot_location = snapshots_parent_location + "\\" + release.name
        print(f"cloning down {repo_ssh} to {snapshots_parent_location}")
        clone_down_repo(
            repo_ssh=repo_ssh, target_parent_location=snapshots_parent_location
        )
        # rename
        os.rename(
            snapshots_parent_location + "\\" + repo_location.split("\\")[-1],
            snapshot_location,
        )
        repo = Repo(snapshot_location)
        print(f"checking out {release.name}")
        repo.git.checkout(release.name)


repo_ssh = "git@github.com:0xdomyz/utube_playlist_mp3_downloader.git"
repo_location = r"C:\Users\yzdom\Projects\utube_playlist_mp3_downloader"
snapshots_parent_location = (
    r"C:\Users\yzdom\Projects\utube_playlist_mp3_downloader_snapshots"
)
clone_down_tags(
    repo_ssh=repo_ssh,
    repo_location=repo_location,
    snapshots_parent_location=snapshots_parent_location,
)

# audit trail via popy paste a master repo, then checkout tags
##############################################################

import shutil


def duplicate_and_checkout_tags(repo_location, snapshots_parent_location):
    Path(snapshots_parent_location).mkdir(parents=True, exist_ok=True)
    releases = get_all_releases(repo_location)
    for release in releases:
        # copy from master repo
        print(f"copying from {repo_location} to {snapshots_parent_location}")
        target_location = snapshots_parent_location + "\\" + release.name
        # Path(target_location).mkdir(parents=True, exist_ok=True)
        shutil.copytree(repo_location, target_location)
        # checkout
        repo = Repo(target_location)
        print(f"checking out {release.name}")
        repo.git.checkout(release.name)


repo_location = r"C:\Users\yzdom\Projects\utube_playlist_mp3_downloader"
snapshots_parent_location = (
    r"C:\Users\yzdom\Projects\utube_playlist_mp3_downloader_snapshots"
)
duplicate_and_checkout_tags(
    repo_location=repo_location, snapshots_parent_location=snapshots_parent_location
)
