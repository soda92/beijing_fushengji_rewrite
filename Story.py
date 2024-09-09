from PySide6 import QtWidgets, QtCore
from story_ui import Ui_Story


class StoryDlg(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Story()
        self.ui.setupUi(self)

        self.messages = [
            "初始化黑客信息....",
            "初始化二环路信息.....",
            "初始化黑市物品......",
            "初始化随机事件......",
            "加载北京实时新闻...."
        ]
        self._count = 0

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
