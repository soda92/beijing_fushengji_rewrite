from PySide6 import QtWidgets
from ui.celebrate import Ui_Form
import random


class CelebrateWindow(QtWidgets.QDialog):
    def __init__(self, score, order):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.messages = [
            self.tr("Outstanding money-maker in Beijing"),
            self.tr("Top 10 outstanding young people in Beijing"),
            self.tr("The coolest reseller in Beijing"),
            self.tr("The money-making master in Beijing"),
            self.tr("Beijing's No. 1 golden finger"),
        ]
        message = random.choice(self.messages)
        self.ui.l_summary.setText(self.ui.l_summary.text().format(score, order))
        self.ui.l_title.setText(self.ui.l_title.text().format(message))

        self.ui.pushButton.clicked.connect(self.check_name)

    def check_name(self):
        name = self.ui.lineEdit.text()
        if name.strip() == "":
            pass
        else:
            self.name = name
            self.close()

    def get_name(self):
        return self.name
