from PySide6 import QtWidgets
from ui.send_money import Ui_SendMoney

class SendMoney(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SendMoney()
        self.ui.setupUi(self)
