from types import MethodType
from orun.test.utils import get_runner
from orun.conf import settings
from base.utils import run_tests


def execute(app: str, report):
    """Execute all founded tests in the app structure."""
    print('\033[92m' + '\033[1m' + f'Executing tests for app {app}' + '\033[0m')
    TestRunner = get_runner(settings)
    runner = TestRunner(interactive=False, parallel=1, pattern='test*.py', failfast=True)
    runner.run_tests = MethodType(run_tests, runner)
    result = runner.run_tests([app])
    report.send_result(result, app)