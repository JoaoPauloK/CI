import os
from unittest.runner import TextTestResult
from orun.test.utils import setup_test_environment


def send_result(result: TextTestResult):
    if len(result.errors) == 0 and len(result.failures) == 0:
        return None
    errors = [error[1].split('\n') for error in result.errors]
    failures = [failure[1].split('\n') for failure in result.failures]
    return format_message({
        'errors': errors, 
        'failures': failures, 
        'nerrors': len(result.errors), 
        'nfailures': len(result.failures)
    })

def format_message(exceptions: dict):
    # Directory to storage temporary files
    tmp_path = os.path.join('..', 'tmp')
    if not os.path.isdir(tmp_path):
        os.mkdir(tmp_path)
    with open(os.path.join(tmp_path, 'test.log'), 'w') as f:
        title = '------------ ERROS ------------\n\n Total: %s\n\n' % exceptions['nerrors']
        f.write(title)
        for error in exceptions['errors']:
            for line in error:
                f.write(f'{line}\n')
        f.write('------------ FALHAS ------------\n\n Total: %s\n\n' % exceptions['nfailures'])
        for failure in exceptions['failures']:
            for line in failure:
                f.write(f'{line}\n')


def run_tests(self, test_labels, extra_tests=None, **kwargs):
    """Custom version of Orun's DiscoverRunner run_tests() method returning the content of results."""
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