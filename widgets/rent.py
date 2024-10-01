from PySide6 import QtWidgets

from ui.rent import Ui_Rent

class Rent(QtWidgets.QDialog):
    def __init__(self, money: int, max_quantity: int):
        super().__init__()
        self.ui = Ui_Rent()
        self.ui.setupUi(self)

        t = self.ui.label_2.text()
        t = t.format(max_quantity, int(money/2), max_quantity + 10)
        self.ui.label_2.setText(t)

        self.ui.ok.clicked.connect(self.accept)
        self.ui.cancel.clicked.connect(self.reject)

