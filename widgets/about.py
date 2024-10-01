from PySide6 import QtWidgets, QtCore
from ui.about import Ui_AboutGame
from widgets.statements import Statement
from widgets.send_money import SendMoney
from widgets.easteregg import EasterEgg


class AboutGame(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AboutGame()
        self.ui.setupUi(self)
        self.show()
        self.ui.send_money.clicked.connect(self.send_money)
        self.ui.show_statement.clicked.connect(self.show_statement)

        self.rclick_times = 0

    def show_statement(self):
        self.statement = Statement()
        self.statement.show()

    def send_money(self):
        self.d_money = SendMoney()
        self.d_money.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.rclick_times += 1
            if self.rclick_times > 5:
                if self.rclick_times > 10:
                    self.easteregg = EasterEgg(True)
                    self.easteregg.show()
                    self.rclick_times = 0
                elif self.rclick_times == 6:
                    self.easteregg = EasterEgg()
                    self.easteregg.show()
        super().mousePressEvent(event)
