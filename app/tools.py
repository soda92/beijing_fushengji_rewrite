import sys
import os
from PySide6 import QtWidgets
from app.models import Status, Item


def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    return hasattr(sys, "gettrace") and sys.gettrace() is not None


def info(title, text: str):
    if getattr(sys, "frozen", False):
        QtWidgets.QMessageBox.information(None, title, text)
    else:
        print(title, text)


def print_dirs():
    application_path = os.path.dirname(__file__)
    runtime_dir = os.path.dirname(sys.executable)
    # determine if application is a script file or frozen exe
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
        runtime_dir = sys._MEIPASS
    cwd = os.getcwd()

    info("application_path", application_path)
    info("runtime_dir", runtime_dir)
    info("cwd", cwd)


def test_dirs():
    from app.defs import Debug

    if debugger_is_active() or Debug:
        print_dirs()


def load_data() -> (Status, list[Item], list[Item]):
    status = Status()
    market_items = []
    my_items = []

    return status, market_items, my_items
