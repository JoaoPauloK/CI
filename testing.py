import os
import subprocess
import importlib
from orun.conf import settings


setup = {
    'project_name': 'teste'
}

# Check if project folder is in pythonpath
if importlib.util.find_spec(setup.get('project_name')) is None:
    import sys
    sys.path.insert(1, os.path.dirname(os.getcwd()))
manage_path = os.path.join('..', 'manage.py')
os.environ['ORUN_SETTINGS_MODULE'] = 'teste.settings'

def execute(app):
    cmd = ['python3', manage_path, 'test']
    if settings.FAILFAST:
        cmd.append('--failfast')
    if settings.NO_INPUT:
        cmd.append('--no-input')
    cmd.append(app)
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        with open('exceptions.log', 'a+') as f:
            f.write(e)

def main():
    for app in settings.TESTED_APPS:
        execute(app)

if __name__ == '__main__':
    main()