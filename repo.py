from git import Repo


repo = Repo('/home/joaopaulo/work/teste/ci')

def check_updates(repo: Repo):
    """ Check if there is any update on remote repository """
    local = repo.head.commit
    remote = repo.remote()

check_updates(repo)