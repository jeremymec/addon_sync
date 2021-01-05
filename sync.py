from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from enum import Enum, auto

class SyncStatus(Enum):
    ERROR = auto()
    UPDATED_FROM_CLOUD = auto()
    UPLOADED_TO_CLOUD = auto()
    NO_CHANGE = auto()

class Sync:

    def __init__(self, base_path, remote_path):

        try:
            self.repo = Repo(base_path)
        except (InvalidGitRepositoryError, NoSuchPathError) as e:
            self.repo = self.clone_repo(base_path, remote_path)

    def clone_repo(self, path, remote):
        addons_repo = Repo.init(path)
        remote = addons_repo.create_remote('origin', url=remote)
        remote.fetch()
        addons_repo.git.checkout('-ft', 'origin/master')
        return addons_repo

    def sync(self):
        sync_info = {'status': SyncStatus.NO_CHANGE}
        remote = self.repo.remote()
        pull_result = remote.pull()
        for fetch_info in pull_result:
            if fetch_info.flags == 128:
                sync_info['status'] = SyncStatus.ERROR
            elif fetch_info.flags != 4:
                sync_info['status'] = SyncStatus.UPDATED_FROM_CLOUD

        self.repo.git.add('.')
        if self.repo.index.diff("HEAD") != []:
            sync_info['status'] = SyncStatus.UPLOADED_TO_CLOUD
        self.repo.index.commit('Addon Update')
        origin = self.repo.remote()
        origin.push()
        return sync_info