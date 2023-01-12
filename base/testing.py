from types import MethodType
from orun.test.utils import get_runner
from orun.conf import settings
from base.utils import run_tests, send_result


def execute(app: str):
    print('\033[92m' + '\033[1m' + f'Executing tests for app {app}' + '\033[0m')
    TestRunner = get_runner(settings)
    runner = TestRunner(interactive=False, parallel=1, pattern='test*.py', failfast=True)
    runner.run_tests = MethodType(run_tests, runner)
    result = runner.run_tests([app])
    send_result(result)