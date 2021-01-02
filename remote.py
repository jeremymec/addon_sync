from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from pathlib import Path

def addons_exist():
    path_to_repo = Path(__file__).parent.absolute().joinpath('addons')

    try:
        Repo(path_to_repo)
        return True
    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        return False

def push_addons():
    path_to_repo = Path(__file__).parent.absolute().joinpath('addons')

    repo = Repo(path_to_repo)

    repo.git.add('.')
    repo.index.commit('Addon Update')
    origin = repo.remote(name='origin')
    origin.push()

def clone_addons(repo_url):
    Repo.clone_from(repo_url, 'addons')

def update_addons():
    path_to_repo = Path(__file__).parent.absolute().joinpath('addons')

    Repo(path_to_repo).remotes.origin.pull()