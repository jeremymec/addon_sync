from git import Repo
from pathlib import Path

def push_addons_to_git():
    path_to_repo = Path(__file__).parent.absolute().joinpath('wow-addons')

    repo = Repo(path_to_repo)

    repo.git.add('.')
    repo.index.commit('Addon Update')
    origin = repo.remote(name='origin')
    origin.push()