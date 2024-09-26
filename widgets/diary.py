from PySide6 import QtWidgets
from ui.diary import Ui_Diary

class Diary(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Diary()
        self.ui.setupUi(self)
