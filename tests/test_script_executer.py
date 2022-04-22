import os

import pytest
from PyQt5 import QtWidgets

from sot_ipython_connection.sot_client import SOTClient
from sot_ipython_connection.app.sot_script_executer import main as script_executer


script_directory = os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def launch_kernel_and_app():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    yield


def test_var_definition():
    kernel_client = SOTClient()

    script_executer([script_directory + "/script_test_1.py"])
    kernel_client.run_python_command("script_var_1")
    kernel_client.run_python_command("script_var_2")

    assert len(kernel_client.cmd_history) == 2

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None

    assert kernel_client.cmd_history[0].stdout == "1"
    assert kernel_client.cmd_history[1].stdout == "2"


def test_multiple_scripts_var_definition():
    kernel_client = SOTClient()

    script_executer([script_directory + "/script_test_2.py",
        script_directory + "/script_test_3.py"])
    kernel_client.run_python_command("script_var_3")
    kernel_client.run_python_command("script_var_4")

    assert len(kernel_client.cmd_history) == 2

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None

    assert kernel_client.cmd_history[0].stdout == "3"
    assert kernel_client.cmd_history[1].stdout == "4"


def test_multiple_scripts_var_redefinition():
    kernel_client = SOTClient()

    script_executer([script_directory + "/script_test_4.py",
        script_directory + "/script_test_5.py"])
    kernel_client.run_python_command("script_var_5")
    kernel_client.run_python_command("script_var_6")

    assert len(kernel_client.cmd_history) == 2

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None

    assert kernel_client.cmd_history[0].stdout == "55"
    assert kernel_client.cmd_history[1].stdout == "6"
