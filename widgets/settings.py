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
