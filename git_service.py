from git import Repo, InvalidGitRepositoryError, NoSuchPathError, GitCommandError
from sync_status import SyncStatus
from shutil import copy2
from pathlib import Path
import os

class GitService:

    def __init__(self, path_to_repo, remote_url):
        self.repo_path = path_to_repo
        try:
            self.repo = Repo(path_to_repo)
        except (InvalidGitRepositoryError, NoSuchPathError):
            self.repo = self.clone_repo(path_to_repo, remote_url)

    def use_local(self):
        self.repo.git.checkout('--ours', '.')

    def use_remote(self):
        self.repo.git.checkout('--theirs', '.')

    def clone_repo(self, path, remote):
        addons_repo = Repo.init(path)
        remote = addons_repo.create_remote('origin', url=remote)
        remote.fetch()
        
        # Check if the repo has a gitignore and create one if it does not
        if not os.path.exists(os.path.join(self.repo_path, '.gitignore')):
            self.create_gitignore()

        try:
            addons_repo.git.checkout('-ft', 'origin/master')
        except GitCommandError:
            # This needs to push somehow

        return addons_repo

    def create_gitignore(self):
        current_path = Path().absolute()
        gitignore_file_path = os.path.join(current_path, 'files', '.gitignore')
        copy2(gitignore_file_path, self.repo_path)

    def commit_local_changes(self):
        self.repo.git.add('.')
        
        try:
            self.repo.git.commit('-m', 'Addon update')
            return SyncStatus.UPLOADED_TO_CLOUD
        except GitCommandError:
            return SyncStatus.NO_CHANGE

    def pull_remote_changes(self):
        remote = self.repo.remote()

        fetch_result = remote.fetch()

        try:
            self.repo.git.merge('origin/master')
        except GitCommandError:
            return SyncStatus.MERGE_CONFLICT

        for fetch_info in fetch_result:
            if fetch_info.flags == 128:
                return SyncStatus.ERROR
            elif fetch_info.flags != 4:
                return SyncStatus.UPDATED_FROM_CLOUD

        return SyncStatus.NO_CHANGE

    def push_changes_to_remote(self):
        origin = self.repo.remote('origin')
        print(origin)
        result = origin.push()
        print(result)
    