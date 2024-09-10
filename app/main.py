from PySide6 import QtWidgets
from app.story import StoryDlg
import sys
from ui.main import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hide()
        self.show_intro()

    def show_intro(self):
        self.dlg = StoryDlg()
        self.dlg.start_sig.connect(self.check_start)
        self.dlg.show()

    def check_start(self):
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
