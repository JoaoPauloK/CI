import os
from .setup import PROJECT_NAME


def env_required(function):
    """Setup the Orun environment to perform framework requiring tasks."""
    def wrapper(*args, **kwargs):
        import sys
        import importlib
        import orun

        os.environ['ORUN_SETTINGS_MODULE'] = f'{PROJECT_NAME}.settings'
        if importlib.util.find_spec(PROJECT_NAME) is None: 
            sys.path.insert(1, os.path.dirname(os.getcwd()))
        orun.setup()
        return function(*args, **kwargs)
    return wrapper