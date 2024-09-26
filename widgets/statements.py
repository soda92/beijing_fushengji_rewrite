from PySide6 import QtWidgets
from ui.statements import Ui_Statements

class Statement(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Statements()
        self.ui.setupUi(self)
