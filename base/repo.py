from git import Repo


repo = Repo('/home/joaopaulo/work/teste/ci')

def is_up_to_date(repo: Repo):
    """ Check if there is any update on remote repository """
    return repo.head.commit.hexsha == repo.remote().refs[0].commit.hexsha