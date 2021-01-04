from git import Repo, InvalidGitRepositoryError, NoSuchPathError

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

    def sync(self):
        remote = self.repo.remote()
        remote.pull()

        self.repo.git.add('.')
        self.repo.index.commit('Addon Update')
        origin = self.repo.remote()
        origin.push()