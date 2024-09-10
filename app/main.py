from PySide6 import QtWidgets
from Story import StoryDlg
import sys

G_SHOWTIPS = 1


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.showTipsAtStartup()

    def showTipsAtStartup(self):
        self.dlg = StoryDlg()
        self.dlg.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    a = [window]
    sys.exit(app.exec())
