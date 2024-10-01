from PySide6 import QtWidgets, QtGui, QtCore
import os
import importlib


class MyInput(QtWidgets.QLineEdit):
    """
    Custom input class for handling input history.
    """

    sig_up = QtCore.Signal()
    sig_down = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.text_changed)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.sig_up.emit()
        elif event.key() == QtCore.Qt.Key.Key_Down:
            self.sig_down.emit()
        super().keyPressEvent(event)

    def text_changed(self):
        "some help"
        if len(self.text()) == 0:
            return


class DebugWidget(QtWidgets.QWidget):
    "The main debug widget layout."

    sig_data = QtCore.Signal(list, list)

    def __init__(self, main_widget=None, commands=(), results=()):
        super().__init__()
        self.main = main_widget

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self.commands_area = QtWidgets.QScrollArea()
        self.commands_area.setWidgetResizable(True)
        self.commands_area_contents = QtWidgets.QWidget()
        self.commands_area.setWidget(self.commands_area_contents)
        self.commands_area_layout = QtWidgets.QVBoxLayout()
        self.commands_area_contents.setLayout(self.commands_area_layout)

        self.commands = list(commands)
        self.results = list(results)

        self.input = MyInput()
        self.input.returnPressed.connect(self.r_eval)

        self.input.sig_up.connect(self.enumerate_previous_command)
        self.input.sig_down.connect(self.enumerate_next_command)

        self._layout.addWidget(self.commands_area)
        self._layout.addWidget(self.input)
        self.input.setFocus()

        self.input_index = 0
        for i in range(len(self.commands)):
            command = QtWidgets.QLabel(self.commands[i])
            command.setWordWrap(True)
            result = QtWidgets.QLabel(self.results[i])
            result.setWordWrap(True)
            self.commands_area_contents.layout().addWidget(command)
            self.commands_area_contents.layout().addWidget(result)

    def enumerate_previous_command(self):
        if len(self.commands) == 0:
            return
        self.input_index -= 1
        if self.input_index < 0:
            self.input_index = 0
        command = self.commands[self.input_index]
        self.input.setText(command)

    def enumerate_next_command(self):
        if len(self.commands) == 0:
            return
        self.input_index += 1
        if self.input_index >= len(self.commands):
            self.input_index = len(self.commands) - 1

        command = self.commands[self.input_index]
        self.input.setText(command)

    def r_eval(self):
        data = self.input.text()
        self.input.clear()
        try:
            r = eval(data)
        except Exception as e:
            r = str(e)
            try:
                exec(data)
            except Exception as e2:
                print(e, e2)
            else:
                self.add_data(data, "eval")
        else:
            self.add_data(data, r)

    def add_data(self, command, result):
        self.commands.append(str(command))
        self.results.append(str(result))
        self.sig_data.emit(self.commands, self.results)
        self.refresh_display()
        self.input_index = len(self.commands)

    def refresh_display(self):
        command = QtWidgets.QLabel(self.commands[-1])
        command.setWordWrap(True)
        result = QtWidgets.QLabel(self.results[-1])
        result.setWordWrap(True)
        self.commands_area_contents.layout().addWidget(command)
        self.commands_area_contents.layout().addWidget(result)

        QtCore.QTimer.singleShot(200, self.scroll)

    def scroll(self):
        scroll_bar = self.commands_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())


class DebugWindowReloader(QtWidgets.QWidget):
    "check modified file, reload debug widget."

    def __init__(self, main=None):
        super().__init__()
        self.main = main

        self.setWindowTitle("Live Debugger")

        self.commands = []  # for persisting input history during reload
        self.results = []

        self.mtime = os.path.getmtime(__file__)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check)
        self.timer.start(1000)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.widget = DebugWidget(self.main, self.commands, self.results)
        self.widget.sig_data.connect(self.slot_data)
        self._layout.addWidget(self.widget)

        self.resize(600, 400)

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
                    self.widget_2 = s.DebugWidget(
                        self.main, self.commands, self.results
                    )
                except Exception as _v:
                    pass
                else:
                    self._layout.removeWidget(self.widget)
                    self.widget.setParent(None)
                    self.widget = self.widget_2
                    self.widget.sig_data.connect(self.slot_data)
                    self._layout.addWidget(self.widget)

    def slot_data(self, commands, results):
        self.commands = commands
        self.results = results


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    widget = DebugWindowReloader()
    widget.show()
    app.exec()
