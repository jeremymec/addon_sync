from git import Repo, InvalidGitRepositoryError, NoSuchPathError, GitCommandError
from sync_status import SyncStatus

class GitService:

    def __init__(self, path_to_repo, remote_url):
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
        addons_repo.git.checkout('-ft', 'origin/master')
        return addons_repo

    def commit_local_changes(self):
        self.repo.git.add('.')
        if self.repo.index.diff('HEAD') != []:
            self.repo.index.commit('Addon Update')
            return SyncStatus.UPLOADED_TO_CLOUD

        return SyncStatus.NO_CHANGE

    def pull_remote_changes(self):
        remote = self.repo.remote()
        try:
            pull_result = remote.pull()
        except GitCommandError:
            return SyncStatus.MERGE_CONFLICT

        for fetch_info in pull_result:
            if fetch_info.flags == 128:
                return SyncStatus.ERROR
            elif fetch_info.flags != 4:
                return SyncStatus.UPDATED_FROM_CLOUD

        return SyncStatus.NO_CHANGE

    def push_changes_to_remote(self):
        origin = self.repo.remote()
        origin.push()
    