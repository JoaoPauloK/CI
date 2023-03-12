import os
import importlib
from git import Repo
from git.exc import InvalidGitRepositoryError
from .decorators import env_required
from .testing import execute
from .setup import TESTED_APPS
from export.export import TestReport

def get_repo(repo_name: str) -> Repo:
    """Return Repo object based on path if it is a valid git repository."""
    try:
        repo = Repo(repo_name)
    except InvalidGitRepositoryError as e:
        raise InvalidGitRepositoryError(
            "Ivalid repository name: %s" % repo_name
        )
    return repo

def is_up_to_date(repo_name: str) -> bool:
    """Check if there is any update on remote repository."""
    print('Checking updated')
    repo = get_repo(repo_name)
    repo.remote().fetch()
    return repo.head.commit.hexsha == repo.remote().refs[0].commit.hexsha

def update_repo(repo: str):
    """Execute pull on the given repository."""
    get_repo(repo).remotes.origin.pull()

@env_required
def perform_tests(test_labels: list=None):
    """Run the automated tests founded in the each app of labels list."""
    # tmp_path = os.path.join('..', 'tmp')
    # tmp_file = os.path.join(tmp_path, 'teste.log')
    # if not os.path.isdir(tmp_path):
    #     os.mkdir(tmp_path)
    # if os.path.isfile(tmp_file):
    #     os.remove(tmp_file)
    test_labels = test_labels or TESTED_APPS
    report = TestReport()
    for app in test_labels:
        execute(app, report)
    if report.has_errors:
        report.send_mail()

@env_required
def get_repo_path(appname: str) -> str:
    """Get the string name of a module and returns its base path."""
    try:
        module = importlib.import_module(appname)
    except ImportError as err:
        raise ImportError(
            "Couldn't import %s. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?" % (appname)
        ) from err
    return os.path.dirname(os.path.dirname(module.__file__))