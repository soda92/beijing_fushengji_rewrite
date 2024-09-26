from PySide6 import QtWidgets, QtCore
from ui.statements import Ui_Statements


class Statement(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Statements()
        self.ui.setupUi(self)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.debug_break)
        self.timer.start(7000)

    def debug_break(self):
        # breakpoint()
        pass
