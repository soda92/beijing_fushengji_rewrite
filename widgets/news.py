from PySide6 import QtWidgets
from ui.news import Ui_News


class News(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_News()
        self.ui.setupUi(self)
