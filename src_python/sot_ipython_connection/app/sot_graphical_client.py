import sys
import os

from PyQt5 import QtWidgets

scriptDirectory = os.path.dirname(__file__)
moduleDirectory = os.path.join(scriptDirectory, '..')
sys.path.append(moduleDirectory)
from sot_client import SOTClient


def main():
    # TODO: launch the qt client
    app = QtWidgets.QApplication.instance() 
    if not app:
        app = QtWidgets.QApplication([])

    kernel_client = SOTClient()
    kernel_client.run_python_command("aaa = 4")
    kernel_client.run_python_command("b = 54")
    print("-----------------")
    kernel_client.show_history()
    print("-----------------")
    kernel_client.show_self_history()
    print()


if __name__ == "__main__":
    main()
