from PySide6 import QtWidgets, QtCore
from ui.bank import Ui_Bank
from ui.money_exchange import Ui_MoneyExchange


class MoneyExchange(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MoneyExchange()
        self.ui.setupUi(self)


class Bank(QtWidgets.QWidget):
    sig_account = QtCore.Signal(int, int)

    def __init__(self, parent=None, cash: int = 0, saving: int = 0):
        super().__init__(parent)
        self.ui = Ui_Bank()
        self.ui.setupUi(self)

        self.cash = cash
        self.saving = saving

        self.ui.label.setText(
            self.tr(
                "Hello customer! Your cash is {}, your deposit is {}, what do you want to do..."
            ).format(self.cash, self.saving)
        )

        self.ui.deposit.clicked.connect(self.deposit)
        self.ui.withdraw.clicked.connect(self.withdraw)

    def deposit(self):
        self.dialog = MoneyExchange()
        self.dialog.ui.label.setText(self.tr("How much money do you deposit?"))
        self.dialog.ui.spinBox.setMinimum(0)
        self.dialog.ui.spinBox.setMaximum(self.cash)
        self.dialog.show()
        self.dialog.ui.pushButton.clicked.connect(self.finish_deposit)

    def finish_deposit(self):
        amount = self.dialog.ui.spinBox.value()
        self.cash -= amount
        self.saving += amount
        self.sig_account.emit(self.cash, self.saving)
        self.dialog.close()
        self.close()

    def withdraw(self):
        self.dialog = MoneyExchange()
        self.dialog.ui.label.setText(self.tr("How much money do you withdraw?"))
        self.dialog.ui.spinBox.setMinimum(0)
        self.dialog.ui.spinBox.setMaximum(self.saving)
        self.dialog.ui.spinBox.setValue(self.saving)
        self.dialog.show()
        self.dialog.ui.pushButton.clicked.connect(self.finish_withdraw)

    def finish_withdraw(self):
        amount = self.dialog.ui.spinBox.value()
        self.saving -= amount
        self.cash += amount
        self.sig_account.emit(self.cash, self.saving)
        self.dialog.close()
        self.close()
