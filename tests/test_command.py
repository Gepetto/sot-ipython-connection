import pytest
from PyQt5 import QtWidgets

from sot_ipython_connection.sot_client import SOTClient


@pytest.fixture(autouse=True)
def launch_kernel_and_app():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    yield
        

def test_var_definition():
    kernel_client = SOTClient()

    kernel_client.run_python_command("cmd_1 = 1")
    kernel_client.run_python_command("cmd_2 = \"abc\"")
    kernel_client.run_python_command("cmd_1")
    kernel_client.run_python_command("cmd_2")

    assert len(kernel_client.cmd_history) == 4

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None
    assert kernel_client.cmd_history[2].stderr == None
    assert kernel_client.cmd_history[3].stderr == None
    
    assert kernel_client.cmd_history[2].stdout == "1"
    assert kernel_client.cmd_history[3].stdout == "'abc'"


def test_var_redefinition():
    kernel_client = SOTClient()

    kernel_client.run_python_command("cmd_3 = 3")
    kernel_client.run_python_command("cmd_3 = 33")
    kernel_client.run_python_command("cmd_3")

    assert len(kernel_client.cmd_history) == 3

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None
    assert kernel_client.cmd_history[2].stderr == None

    assert kernel_client.cmd_history[2].stdout == "33"


def test_operations():
    kernel_client = SOTClient()

    kernel_client.run_python_command("cmd_4 = 4")
    kernel_client.run_python_command("cmd_5 = 5")
    kernel_client.run_python_command("cmd_6 = cmd_4 + cmd_5")
    kernel_client.run_python_command("cmd_6")

    assert len(kernel_client.cmd_history) == 4

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None
    assert kernel_client.cmd_history[2].stderr == None
    assert kernel_client.cmd_history[3].stderr == None

    assert kernel_client.cmd_history[3].stdout == "9"
    

def test_undefined_var():
    kernel_client = SOTClient()

    kernel_client.run_python_command("undefined_var")

    assert len(kernel_client.cmd_history) == 1
    assert kernel_client.cmd_history[0].stdout == None
    assert kernel_client.cmd_history[0].stderr != None
    

def test_import():
    kernel_client = SOTClient()

    kernel_client.run_python_command("import math")
    kernel_client.run_python_command("fabs(-4)")

    assert len(kernel_client.cmd_history) == 2

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None

    assert kernel_client.cmd_history[1].stdout == "4.0"
    

def test_object():
    kernel_client = SOTClient()

    kernel_client.run_python_command("\
        class cmd_test_class:\n \
            \tdef __init__(self, attr_1):\n \
                \t\tself.attr_1 = attr_1\n \
                \t\tself.attr_2 = 2\n \
                \t\tself.attr_3 = 3\n \
    ")

    kernel_client.run_python_command("obj_1 = cmd_test_class(\"abc\")")
    kernel_client.run_python_command("obj_1.attr_3 = 33")
    kernel_client.run_python_command("obj_1.attr_1")
    kernel_client.run_python_command("obj_1.attr_2")
    kernel_client.run_python_command("obj_1.attr_3")

    assert len(kernel_client.cmd_history) == 6

    assert kernel_client.cmd_history[0].stderr == None
    assert kernel_client.cmd_history[1].stderr == None
    assert kernel_client.cmd_history[2].stderr == None
    assert kernel_client.cmd_history[3].stderr == None
    assert kernel_client.cmd_history[4].stderr == None
    assert kernel_client.cmd_history[5].stderr == None
    
    assert kernel_client.cmd_history[3].stdout == "'abc'"
    assert kernel_client.cmd_history[4].stdout == "2"
    assert kernel_client.cmd_history[5].stdout == "33"
