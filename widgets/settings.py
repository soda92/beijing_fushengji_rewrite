from PySide6 import QtWidgets
from ui.settings import Ui_Settings

class Settings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(lambda: self.close())
        self.ui.pushButton_2.clicked.connect(lambda: self.close())
