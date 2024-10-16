from PySide6 import QtWidgets, QtCore
from app.tools import load


class AboutGame(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = load("ui.about").Ui_AboutGame()
        self.ui.setupUi(self)
        self.show()
        self.ui.send_money.clicked.connect(self.send_money)
        self.ui.show_statement.clicked.connect(self.show_statement)

        self.rclick_times = 0

    def show_statement(self):
        self.statement = load("widgets.simple_dialogs").Statement()
        self.statement.show()

    def send_money(self):
        self.d_money = load("widgets.simple_dialogs").SendMoney()
        self.d_money.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.rclick_times += 1
            if self.rclick_times > 5:
                if self.rclick_times > 10:
                    self.easteregg = load("widgets.simple_dialogs").EasterEgg(True)
                    self.easteregg.show()
                    self.rclick_times = 0
                elif self.rclick_times == 6:
                    self.easteregg = load("widgets.simple_dialogs").EasterEgg()
                    self.easteregg.show()
        super().mousePressEvent(event)
