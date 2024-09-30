from PySide6 import QtWidgets, QtGui, QtCore
import os
import importlib


class MyInput(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.text_changed)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.overlay.hide()
        super().keyPressEvent(event)

    def text_changed(self):
        "some help"
        if len(self.text()) == 0:
            return


class DebugWidget(QtWidgets.QWidget):
    def __init__(self, main_widget=None):
        super().__init__()
        self.main = main_widget

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self.texts = QtWidgets.QTextBrowser()
        self.data = []
        self.texts.setText("--990   999 99021")

        self.input = MyInput()
        self.input.returnPressed.connect(self.r_eval)

        self._layout.addWidget(self.texts)
        self._layout.addWidget(self.input)

    def r_eval(self):
        data = self.input.text()
        self.input.clear()
        try:
            r = eval(data)
        except Exception as e:
            print(e)
        else:
            self.data.append(data)
            self.data.append(r)
            self.texts.setText("\n".join(map(str, self.data)))


class DebugWindowReloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mtime = os.path.getmtime(__file__)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check)
        self.timer.start(1000)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.widget = DebugWidget()
        self._layout.addWidget(self.widget)

    def check(self):
        mtime = os.path.getmtime(__file__)
        if mtime != self.mtime:
            self.mtime = mtime

            try:
                s = importlib.import_module("widgets.debug_window")
                s = importlib.reload(s)
            except Exception as _:
                pass
            else:
                try:
                    self.widget_2 = s.DebugWidget()
                except:
                    pass
                else:
                    self._layout.removeWidget(self.widget)
                    self.widget.setParent(None)
                    self.widget = self.widget_2
                    self._layout.addWidget(self.widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    widget = DebugWindowReloader()
    widget.show()
    app.exec()
