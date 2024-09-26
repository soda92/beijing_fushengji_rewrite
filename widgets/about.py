from PySide6 import QtWidgets
from ui.about import Ui_AboutGame
from widgets.statements import Statement
from widgets.send_money import SendMoney

class AboutGame(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AboutGame()
        self.ui.setupUi(self)
        self.show()
        self.ui.send_money.clicked.connect(self.send_money)
        self.ui.show_statement.clicked.connect(self.show_statement)
    
    def show_statement(self):
        self.statement = Statement()
        self.statement.show()

    def send_money(self):
        self.d_money = SendMoney()
        self.d_money.show()
