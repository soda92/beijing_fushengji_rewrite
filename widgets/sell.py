from ui.sell import Ui_Sell
from PySide6 import QtWidgets
from app.models import Item, get_item_name


class Sell(QtWidgets.QWidget):
    def __init__(self, item: Item):
        super().__init__()
        self.item = item

        self.ui = Ui_Sell()
        self.ui.setupUi(self)
        self.item = item

        self.ui.spinBox.setMinimum(1)
        self.ui.spinBox.setMaximum(item.quantity)
        self.ui.spinBox.setValue(item.quantity)

        self.ui.label.setText(
            self.tr("You have {} {}, how many do you want to sell?").format(
                item.quantity, get_item_name(item)
            )
        )
        self.ui.pushButton.clicked.connect(self.close)
