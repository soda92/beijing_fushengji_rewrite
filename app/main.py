import os
import platform
import sys
import widgets.mainwindow as mainwindow
from PySide6 import QtWidgets, QtCore
import argparse
from console.mainwindow import main as main_cli

def main_gui():
    if platform.system() == "Linux":
        # this will enable automaic load of fcitx plugin
        os.environ["QT_PLUGIN_PATH"] = "/usr/lib/qt6/plugins/"
    app = QtWidgets.QApplication(sys.argv)
    translator = QtCore.QTranslator()
    translator.load(":/translations/cn.qm")
    app.installTranslator(translator)

    _window = mainwindow.MainWindow()
    _window.show()
    sys.exit(app.exec())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--console", action="store_true", default=False)
    args = parser.parse_args()
    if args.console:
        main_cli()
    else:
        main_gui()


if __name__ == "__main__":
    main()
