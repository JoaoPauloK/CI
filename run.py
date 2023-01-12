import time
from base.repo import is_up_to_date, run_tests, get_repo_path, update_repo
from base.setup import TESTED_APPS, FETCH_TIME


def watch():
    while True:
        for app in TESTED_APPS:
            repo = get_repo_path(app)
            if not is_up_to_date(repo):
                print('Change detected, updating and testing...')
                update_repo(repo)
                run_tests()
        print('waiting %s seconds...' % FETCH_TIME)
        time.sleep(FETCH_TIME)           

if __name__ == '__main__':
    watch()