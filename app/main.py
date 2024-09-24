from PySide6 import QtWidgets, QtGui, QtCore
from app.story import StoryDlg
import sys
from ui.main import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        font_id = QtGui.QFontDatabase.addApplicationFont(":/FONTS/font.ttf")
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setStyleSheet(
            """
            QLabel, QPushButton {
                font: 12pt {family};
            }
            """.replace(
                "{family}", family
            )
        )
        self.setWindowIcon(QtGui.QIcon(":/ICON/icon.ico"))
        import os

        hide_intro = os.environ.get("HIDE_INTRO", False)
        if hide_intro == False:
            self.hide()
            self.show_intro()
        else:
            self.show()
        self.move(
            QtWidgets.QApplication.screens()[0].geometry().center()
            - self.rect().center()
        )
        self.ui.cybercafe.triggered.connect(self.enter_cafe)

    def enter_cafe(self):
        from app.cybercafe import CyberCafe

        self.cafe = CyberCafe()
        self.cafe.show()

    def show_intro(self):
        self.dlg = StoryDlg()
        self.dlg.start_sig.connect(self.check_start)
        self.dlg.show()

    def check_start(self):
        self.show()


def main():
    import os, platform
    if platform.system() == "Linux":
        # this will enable automaic load of fcitx plugin
        os.environ["QT_PLUGIN_PATH"] = "/usr/lib/qt6/plugins/"
    app = QtWidgets.QApplication(sys.argv)
    print(QtCore.QLocale.system().name())
    translator = QtCore.QTranslator()
    translator.load(":/translations/cn.qm")
    app.installTranslator(translator)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
