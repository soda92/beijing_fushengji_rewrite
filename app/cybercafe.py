from PySide6 import QtWidgets
from ui.net_cafe import Ui_Dialog


class CyberCafe(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()



if __name__ == "__main__":
    app = QtWidgets.QApplication()
    cafe = CyberCafe()
    cafe.show()
    app.exec()