from ui.buy import Ui_Buy
from PySide6 import QtWidgets
from app.models import Item, get_item_name


class Buy(QtWidgets.QWidget):
    def __init__(self, cash: int, item: Item, is_full: bool):
        super().__init__()
        self.cash = cash
        self.item = item

        self.ui = Ui_Buy()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)

        if not is_full:
            max_count = self.cash // self.item.price

            self.ui.spinBox.setMinimum(1)
            self.ui.spinBox.setMaximum(max_count)
            self.ui.spinBox.setValue(max_count)

            self.ui.label.setText(
                self.tr(
                    "Your cash is RMB {}, which can be used to buy up to {} {}."
                ).format(self.cash, max_count, get_item_name(item))
            )
        else:
            self.ui.spinBox.setValue(0)
            self.ui.spinBox.setMinimum(0)
            self.ui.spinBox.setMaximum(0)
            self.ui.label.setText(
                self.tr(
                    "Your cash is RMB {}, the house you rented is full of stuff, so you can't get any more stock. \nTo expand your business, it is recommended that you rent a bigger house."
                ).format(self.cash)
            )
