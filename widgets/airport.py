from PySide6 import QtWidgets
from ui.airport import Ui_Airport

class Airport(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Airport()
        self.ui.setupUi(self)
