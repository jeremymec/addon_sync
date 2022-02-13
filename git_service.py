import os
from enum import Enum, auto
from pathlib import Path
from gitignore_service import create_gitignore_including

from git import (GitCommandError, InvalidGitRepositoryError, NoSuchPathError,
                 Repo)

from sync_status import SyncStatus


class InitRepoResult(Enum):
    REPO_EXISTS = auto()
    CLONE_REPO = auto()
    UPLOAD_TO_BLANK_REPO = auto()


class GitService:
    def __init__(self, repo, path_to_repo, remote_url):
        self.repo = repo
        self.repo_path = path_to_repo
        self.remote_url = remote_url

    @staticmethod
    def create_service(path_to_repo, remote_url, objects_tracked):
        result = None
        repo = None

        try:
            repo = Repo(path_to_repo)
            result = InitRepoResult.REPO_EXISTS
        except (InvalidGitRepositoryError, NoSuchPathError):
            addons_repo = Repo.init(path_to_repo)
            remote = addons_repo.create_remote("origin", url=remote_url)
            remote.fetch()

            # Check if the repo has a gitignore and create one if it does not
            if not os.path.exists(os.path.join(path_to_repo, ".gitignore")):
                print("Creating gitignore")
                GitService.create_gitignore(path_to_repo, objects_tracked)

            try:
                addons_repo.git.checkout("-ft", "origin/master")
                result = InitRepoResult.CLONE_REPO
            except GitCommandError:
                addons_repo.git.add(".")
                addons_repo.git.commit("-m", "Initial Addon Commit")
                addons_repo.git.push("--set-upstream", remote, addons_repo.head)
                result = InitRepoResult.UPLOAD_TO_BLANK_REPO

        service = GitService(repo, path_to_repo, remote_url)
        return {"service": service, "result": result}

    def use_local(self):
        self.repo.git.checkout("--ours", ".")

    def use_remote(self):
        self.repo.git.checkout("--theirs", ".")

    @staticmethod
    def create_gitignore(repo_path, objects_tracked):
        gitignore_string = create_gitignore_including(objects_tracked)
        gitignore_path = Path.joinpath(repo_path, Path('.gitignore'))
        
        with open(gitignore_path, "w") as f:
            f.write(gitignore_string)

        f.close()

    def commit_local_changes(self):
        self.repo.git.add(".")

        try:
            self.repo.git.commit("-m", "Addon update")
            return SyncStatus.UPLOADED_TO_CLOUD
        except GitCommandError:
            return SyncStatus.NO_CHANGE

    def pull_remote_changes(self):
        remote = self.repo.remote()

        fetch_result = remote.fetch()

        try:
            self.repo.git.merge("origin/master")
        except GitCommandError:
            return SyncStatus.MERGE_CONFLICT

        for fetch_info in fetch_result:
            if fetch_info.flags == 128:
                return SyncStatus.ERROR
            elif fetch_info.flags != 4:
                return SyncStatus.UPDATED_FROM_CLOUD

        return SyncStatus.NO_CHANGE

    def push_changes_to_remote(self):
        origin = self.repo.remote("origin")
        print(origin)
        result = origin.push()
        print(result)
