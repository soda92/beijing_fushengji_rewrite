from ui.beijing_intro import Ui_Form
from PySide6 import QtWidgets


class BeijingIntro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.close)
