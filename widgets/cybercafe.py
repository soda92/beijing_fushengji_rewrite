from PySide6 import QtWidgets
from ui.net_cafe import Ui_CyberCafe


class CyberCafe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CyberCafe()
        self.ui.setupUi(self)
        self.show()

        self.ui.leave_cybercafe.clicked.connect(lambda _: self.close())


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    cafe = CyberCafe()
    cafe.show()
    app.exec()
