from PySide6 import QtWidgets, QtCore, QtGui
from ui.story import Ui_Story


class StoryDlg(QtWidgets.QWidget):
    start_sig: QtCore.Signal = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Story()
        self.ui.setupUi(self)
        font_id = QtGui.QFontDatabase.addApplicationFont(":/FONTS/test-font.ttf")
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setStyleSheet(
            """
            QLabel, QPushButton {
                font: 12pt {family};
            }
            """.replace(
                "{family}", "MiSans"
            )
        )
        self.setWindowIcon(QtGui.QIcon(":/ICON/icon.ico"))

        self.ui.startGame.clicked.connect(self.start_game)
        self.ui.startGame.setEnabled(False)

        self.setWindowFlag(
            self.windowFlags() | QtCore.Qt.WindowType.FramelessWindowHint
        )

        self.messages = [
            "初始化黑客信息....",
            "初始化二环路信息.....",
            "初始化黑市物品......",
            "初始化随机事件......",
            "加载北京实时新闻....",
        ]
        self._count = 1
        self.ui.statusText.setText(self.messages[0])

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_message)
        self.timer.setInterval(330)
        self.timer.start()

    def update_message(self):
        if self._count < 5:
            self.ui.statusText.setText(self.messages[self._count])
            self._count += 1
        else:
            self.timer.stop()
            self.processHelpFile()
            QtCore.QTimer.singleShot(
                330,
                self.finish_init,
            )

    def finish_init(self):
        self.ui.statusText.setText("游戏初始化完毕,准备进入北京...")
        self.ui.startGame.setEnabled(True)

    def processHelpFile(self):
        self.ui.statusText.setText("初始化帮助信息....")
        from pathlib import Path

        CURRENT = Path(__file__).resolve().parent
        help_file_encrypted = CURRENT.parent.joinpath("helpinfo")

        from app.tools import test_dirs

        test_dirs()
        content = help_file_encrypted.read_bytes()
        real_content = bytearray([i ^ 0x52 for i in content]).decode("GB2312")
        help_file_encrypted.parent.joinpath("help.html").write_text(
            real_content, encoding="utf8"
        )

    def start_game(self):
        self.start_sig.emit(True)
        self.close()