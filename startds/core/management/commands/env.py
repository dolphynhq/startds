import os
import shutil
import subprocess
import startds
from startds.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Sets up a data-science virtual environment"

    def handle(self, *args, **options):
        '''
        Implement the logic for starting the data science environment.
        For now, we only use venv to manage the environment. 
        But for more advanced control over the environment, we need to use pipenv/poetry/pip-compile,pip-sync
        '''
        if options is None or options.get('f') is None or options.get('f') == []:
            path_to_requirements_file = 'requirements.txt'
        else:
            path_to_requirements_file = options.get('f')[0]
        

        curr_dir = os.getcwd()
        exp_name = os.getcwd().split('/')[-1]

        command0 = f"cd {curr_dir}"
        
        command1 = "python -m venv .venv"
        command2 = "source .venv/bin/activate"
        commandpip = "pip install --upgrade pip"
        command_internal_1 = "pip install -e ."
        command_internal_2 = "pip install pytest python-dotenv"

        command3 = '''
        pip install \
        apache-airflow==1.10.12 \
        --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
        '''
        command_req = f"pip install -r {path_to_requirements_file} --use-feature=2020-resolver"

        if os.path.isdir(f'{curr_dir}/{exp_name}/src/_orchestrate'):
            command_airflow = f'''
            cd {curr_dir}/{exp_name}/src/_orchestrate/airflow;
            export AIRFLOW_HOME={curr_dir}/{exp_name}/src/_orchestrate/airflow ;
            airflow initdb;
            '''
        else:
            command_airflow = ''

        try:
            # subprocess.DEVNULL  subprocess.PIPE
            subprocess.run(f"{command0}; {command1}; {command2}; {commandpip}; {command_internal_1}; {command_internal_2}; {command_req}; {command3} {command_airflow}", shell=True)
        except Exception as e:
            print(e)

        



