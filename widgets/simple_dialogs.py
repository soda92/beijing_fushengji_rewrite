from PySide6 import QtWidgets
import importlib


class Airport(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        import ui.airport

        importlib.reload(ui.airport)
        self.ui = ui.airport.Ui_Airport()
        self.ui.setupUi(self)


class BeijingIntro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        import ui.beijing_intro

        importlib.reload(ui.beijing_intro)
        self.ui = ui.beijing_intro.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.close)


class CyberCafe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        import ui.net_cafe

        importlib.reload(ui.net_cafe)
        self.ui = ui.net_cafe.Ui_CyberCafe()
        self.ui.setupUi(self)
        self.show()

        self.ui.leave_cybercafe.clicked.connect(lambda _: self.close())


from PySide6 import QtWidgets
from ui.diary import Ui_Diary


class Diary(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Diary()
        self.ui.setupUi(self)


from PySide6 import QtWidgets

from ui.easteregg import Ui_Form


class EasterEgg(QtWidgets.QWidget):
    def __init__(self, detail=False):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)

        if not detail:
            self.ui.label.setText(
                self.tr(
                    "Author: Guo Xianghao, male, born in April 1970, graduated from Beijing University of Posts and Telecommunications in 1998 with a Ph.D. in artificial intelligence and natural language processing. Currently engaged in natural language processing research and software development. Loves games so much that he develops his own. Lived in Beijing for more than 10 years."
                )
            )
        else:
            self.ui.label.setText(
                self.tr(
                    "I love nature, art, and literature. I mainly use C/C++ for programming, but I am also very familiar with 80x86 assembly language. I once wrote a computer virus for my girlfriend (now the mother of my child). I am also proficient in LISP and Prolog languages, and have in-depth research on information retrieval technology and concept retrieval technology."
                )
            )


from PySide6 import QtWidgets
from ui.news import Ui_News


class News(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_News()
        self.ui.setupUi(self)


from PySide6 import QtWidgets

from ui.rent import Ui_Rent


class Rent(QtWidgets.QDialog):
    def __init__(self, money: int, max_quantity: int):
        super().__init__()
        self.ui = Ui_Rent()
        self.ui.setupUi(self)

        t = self.ui.label_2.text()
        t = t.format(max_quantity, int(money / 2), max_quantity + 10)
        self.ui.label_2.setText(t)

        self.ui.ok.clicked.connect(self.accept)
        self.ui.cancel.clicked.connect(self.reject)


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


from PySide6 import QtWidgets
from ui.send_money import Ui_SendMoney


class SendMoney(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SendMoney()
        self.ui.setupUi(self)


from PySide6 import QtWidgets, QtCore
from ui.settings import Ui_Settings


class Settings(QtWidgets.QWidget):
    sig_settings = QtCore.Signal(bool, bool)

    def __init__(
        self, parent=None, allow_hacker: bool = False, turn_off_sound: bool = False
    ):
        super().__init__(parent)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.save_settings)
        self.ui.pushButton_2.clicked.connect(lambda: self.close())
        self.ui.allow_hacker.setChecked(allow_hacker)
        self.ui.turn_off_sound.setChecked(turn_off_sound)

    def save_settings(self):
        allow_hacker = self.ui.allow_hacker.isChecked()
        turn_off_sound = self.ui.turn_off_sound.isChecked()
        self.sig_settings.emit(allow_hacker, turn_off_sound)
        self.close()


from PySide6 import QtWidgets
from ui.text_editor import Ui_TextEditor


class TextEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TextEditor()
        self.ui.setupUi(self)
        self.move(
            QtWidgets.QApplication.screens()[0].geometry().center()
            - self.rect().center()
        )
        self.ui.check_grammar.setFocus()
        self.ui.check_grammar.clicked.connect(self.check_grammar)

    def check_grammar(self):
        QtWidgets.QMessageBox.information(
            self,
            self.tr("Grammar"),
            self.tr(
                'Spell check suggestion: "Fragrant air" changed to "Fresh air"; "Boss" changed to "Boss lady".'
            ),
            QtWidgets.QMessageBox.StandardButton.Ok,
        )


from PySide6 import QtWidgets, QtCore
from ui.statements import Ui_Statements


class Statement(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Statements()
        self.ui.setupUi(self)


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
