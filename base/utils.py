import os
from datetime import datetime
from unittest.runner import TextTestResult
from orun.test.utils import setup_test_environment
from export.export import TestReport


def send_result(result: TextTestResult, appname: str):
    if len(result.errors) == 0 and len(result.failures) == 0:
        return
    errors = [error[1].split('\n') for error in result.errors]
    failures = [failure[1].split('\n') for failure in result.failures]
    export_result({
        'appname': appname,
        'errors': errors, 
        'failures': failures, 
        'nerrors': len(result.errors), 
        'nfailures': len(result.failures)
    })

def export_result(result):
    rep = TestReport(result)
    rep.export()
    
def format_message(exceptions: dict):
    # Directory to storage temporary files
    tmp_path = os.path.join('..', 'tmp')
    tmp_file = os.path.join(tmp_path, 'teste.log')
    # if not os.path.isdir(tmp_path):
    #     os.mkdir(tmp_path)
    # if os.path.isfile(tmp_file):
    #     os.remove(tmp_file)
    with open(tmp_file, 'a+') as f:
        f.write('Testes executados para o app %s em %s\n\n' % (exceptions['appname'], datetime.now().ctime()))
        f.write('------------ ERROS ------------\n Total: %s\n\n' % exceptions['nerrors'])
        for error in exceptions['errors']:
            for line in error:
                f.write(f'{line}\n')
        f.write('------------ FALHAS ------------\n Total: %s\n\n' % exceptions['nfailures'])
        for failure in exceptions['failures']:
            for line in failure:
                f.write(f'{line}\n')

def run_tests(self, test_labels, extra_tests=None, **kwargs):
    """Custom version of Orun's DiscoverRunner run_tests method returning the content of results."""
    self.setup_test_environment()
    suite = self.build_suite(test_labels, extra_tests)
    databases = self.get_databases(suite)
    old_config = self.setup_databases(aliases=databases)
    run_failed = False
    try:
        result = self.run_suite(suite)
    except Exception:
        run_failed = True
        raise
    finally:
        try:
            self.teardown_databases(old_config)
            self.teardown_test_environment()
        except Exception:
            if not run_failed:
                raise
    return result