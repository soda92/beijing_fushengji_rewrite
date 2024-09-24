from PySide6 import QtCore, QtMultimedia
import sys
import main_rc

class X(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.effect = QtMultimedia.QSoundEffect()
        self.effect.setSource(QtCore.QUrl.fromLocalFile(":/SND/sound/vomit.wav"))
        self.effect.play()
        QtCore.QTimer.singleShot(1200, lambda: sys.exit())


if __name__ == "__main__":
    app = QtCore.QCoreApplication(sys.argv)
    x = X()
    app.exec()
