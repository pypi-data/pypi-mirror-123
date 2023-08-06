import os
import subprocess
import sys


def execute_pytest_testcases(arguments):
    sys.path.append(os.getcwd())

    pytest_file_list = list()
    for pytest_file in arguments.files_or_dir:
        pytest_file_list.append(pytest_file)

    command = [sys.executable, '-m', 'pytest', '-v']
    command += ['--pistar_dir=' + arguments.output]
    command += pytest_file_list

    process = subprocess.Popen(command)

    process.communicate()
