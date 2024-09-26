from PySide6 import QtWidgets, QtGui, QtCore, QtMultimedia
from widgets.story import StoryDlg
from ui.main import Ui_MainWindow
from widgets.cybercafe import CyberCafe
from widgets.about import AboutGame
from widgets.settings import Settings
from widgets.airport import Airport
from app.tools import load_data


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        font_id = QtGui.QFontDatabase.addApplicationFont(":/FONTS/font.ttf")
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setStyleSheet(
            """
            QLabel, QPushButton {
                font: 12pt {family};
            }
            """.replace(
                "{family}", family
            )
        )
        self.setWindowIcon(QtGui.QIcon(":/ICON/icon.ico"))
        import os

        self.hide()

        hide_intro = os.environ.get("HIDE_INTRO", False)
        if not hide_intro:
            self.show_intro()
        else:
            self.show()
        self.move(
            QtWidgets.QApplication.screens()[0].geometry().center()
            - self.rect().center()
        )
        self.ui.cybercafe.triggered.connect(self.enter_cafe)
        self.ui.p_netcafe.clicked.connect(self.enter_cafe)

        self.ui.exit_game.triggered.connect(self.close)
        self.ui.buy.clicked.connect(self.buy)
        self.ui.sell.clicked.connect(self.sell)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.scroll)
        self.t_pos = 0
        QtCore.QTimer.singleShot(7000, lambda: self.timer.start())
        self.ui.ticker.enterEvent = lambda _: self.timer.stop()
        self.ui.ticker.leaveEvent = lambda _: self.timer.start()

        self.ui.about.triggered.connect(self.show_about)
        self.ui.airport.triggered.connect(self.go_airport)
        self.ui.settings.triggered.connect(self.show_settings)

        self.init_data()

    def show_settings(self):
        self.d_settings = Settings()
        self.d_settings.show()

    def go_airport(self):
        self.d_airport = Airport()
        self.d_airport.show()

    def show_about(self):
        self.about_game = AboutGame()
        self.about_game.show()

    def init_data(self):
        status, market_items, my_items = load_data()
        self.ui.cash.display(status.cash)
        self.ui.debt.display(status.debt)
        self.ui.health.display(status.health)
        self.ui.fame.display(status.fame)
        self.ui.saving.display(status.saving)

    def play_sound(self, name: str):
        # the "self" is important because sound will run in the background
        self.effect = QtMultimedia.QSoundEffect()
        self.effect.setSource(QtCore.QUrl.fromLocalFile(f":/SND/sound/{name}"))
        self.effect.setLoopCount(1)
        self.effect.setVolume(0.8)
        self.effect.play()

    def buy(self):
        pass
        self.play_sound("buy.wav")

    def sell(self):
        pass
        self.play_sound("money.wav")

    def scroll(self):
        self.t_pos += 1.1
        bar = self.ui.ticker.horizontalScrollBar()
        bar.setValue(int(self.t_pos))
        if self.t_pos > bar.maximum():
            self.timer.stop()
            self.timer_restart = QtCore.QTimer()
            self.timer_restart.timeout.connect(self.restart_scroll)
            self.timer_restart.setSingleShot(True)
            self.timer_restart.start(60 * 1000)

    def restart_scroll(self):
        self.t_pos = 0
        QtCore.QTimer.singleShot(7000, lambda: self.timer.start())

    def enter_cafe(self):
        self.cafe = CyberCafe()
        self.cafe.show()

    def show_intro(self):
        self.dlg = StoryDlg()
        self.dlg.start_sig.connect(self.check_start)
        self.dlg.show()

    def check_start(self):
        self.show()
