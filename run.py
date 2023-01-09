from base.repo import is_up_to_date
from git import Repo

if __name__ == '__main__':
    if is_up_to_date(Repo('/home/joaopaulo/work/teste/ci')):
        print('Updated!')
    else:
        print('Not updated!')