from unittest import TestCase
import os
from pathlib import PurePosixPath, Path

from sot_ipython_connection.sot_kernel import SOTKernel
from sot_ipython_connection.sot_client import SOTClient
from sot_ipython_connection.app.sot_script_executer import main as script_executer

import nest_asyncio
nest_asyncio.apply()


current_script_directory = str(Path(__file__).resolve().parent)
input_scripts_dir = str(Path(__file__).resolve().parent/'input_scripts')


class TestScriptExecuter(TestCase):

    @classmethod
    def setup_class(self):
        # Launching the kernel in a subprocess
        self._kernel = SOTKernel()
        self._kernel.run_non_blocking()

    @classmethod
    def teardown_class(self):
        # Terminating the kernel's subprocess
        self._kernel._terminate_kernel_subprocess()


    def test_var_definition(self):
        kernel_client = SOTClient()

        script_path = str(Path(input_scripts_dir)/'script_test_1.py')
        script_executer([script_path])
        kernel_client.run_python_command("script_var_1")
        kernel_client.run_python_command("script_var_2")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == 1
        assert kernel_client.cmd_history[1].result == 2


    def test_multiple_scripts_var_definition(self):
        kernel_client = SOTClient()

        script_paths = [
            str(Path(input_scripts_dir)/'script_test_2.py'),
            str(Path(input_scripts_dir)/'script_test_3.py')
        ]
        script_executer(script_paths)
        kernel_client.run_python_command("script_var_3")
        kernel_client.run_python_command("script_var_4")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == 3
        assert kernel_client.cmd_history[1].result == 4


    def test_multiple_scripts_var_redefinition(self):
        kernel_client = SOTClient()

        script_paths = [
            str(Path(input_scripts_dir)/'script_test_4.py'),
            str(Path(input_scripts_dir)/'script_test_5.py')
        ]
        script_executer(script_paths)
        kernel_client.run_python_command("script_var_5")
        kernel_client.run_python_command("script_var_6")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == 55
        assert kernel_client.cmd_history[1].result == 6


    def test_local_script(self):
        # Launching the client in another directory
        os.chdir('../')
        kernel_client = SOTClient()
        
        # Getting the test script's path (relative to where the client was launched)
        new_path_to_test_script_dir = str(PurePosixPath(input_scripts_dir).
            relative_to(Path.cwd()))

        script_paths = [
            str(Path(new_path_to_test_script_dir)/'script_test_6.py'),
            str(Path(new_path_to_test_script_dir)/'script_test_7.py')
        ]
        
        script_executer(script_paths + ['--local'])

        kernel_client.run_python_command("script_var_7")
        kernel_client.run_python_command("script_var_8")

        assert len(kernel_client.cmd_history) == 2

        assert kernel_client.cmd_history[0].stderr == None
        assert kernel_client.cmd_history[1].stderr == None

        assert kernel_client.cmd_history[0].stdout == None
        assert kernel_client.cmd_history[1].stdout == None

        assert kernel_client.cmd_history[0].result == 7
        assert kernel_client.cmd_history[1].result == 8
