from PySide6 import QtWidgets, QtGui, QtCore
import ui.mainwindow as ui_mainwindow
import ui.main_widget
import widgets.main_widget as main_widget
from widgets.beijing_intro import BeijingIntro


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(":/ICON/icon.ico"))

        self.app = app
        self.translator = QtCore.QTranslator()
        self.translator.load(":/translations/cn.qm")
        self.app.installTranslator(self.translator)
        self.init()

        from app.tools import debugger_is_active

        if debugger_is_active():
            from widgets.debug_window import DebugWindowReloader

            self.debug_window = DebugWindowReloader(self.widget)
            self.debug_window.show()

    def init(self):
        self.ui = ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.widget = main_widget.MainWidget()
        self.widget.hide()
        self.widget.sig_time_pass.connect(self.set_title)
        self.widget.sig_close.connect(self.close)
        self.setCentralWidget(self.widget)
        self.widget.show()

        font_id = QtGui.QFontDatabase.addApplicationFont(":/FONTS/font.ttf")
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setStyleSheet(
            """
            QLabel, QPushButton, QTextBrowser, QGroupBox, QTextEdit, QRadioButton {{
                font: 12pt {family};
            }}
            """.format(family=family)
        )
        self.ui.menubar.setFont(QtGui.QFont(family, 14))
        self.ui.menu.setFont(QtGui.QFont(family, 14))
        self.ui.menu_2.setFont(QtGui.QFont(family, 14))
        self.ui.menu_3.setFont(QtGui.QFont(family, 14))

        self.ui.post_office.triggered.connect(self.widget.pay_debt)
        self.ui.hospital.triggered.connect(self.widget.enter_hospital)
        self.ui.bank.triggered.connect(self.widget.enter_bank)
        self.ui.about.triggered.connect(self.widget.show_about)
        self.ui.airport.triggered.connect(self.widget.go_airport)
        self.ui.settings.triggered.connect(self.widget.show_settings)
        self.ui.exit_game.triggered.connect(self.widget.close)
        self.ui.exit_game.triggered.connect(self.close)
        self.ui.cybercafe.triggered.connect(self.widget.enter_cafe)
        self.ui.top_players.triggered.connect(self.widget.show_top_players)
        self.ui.new_game.triggered.connect(self.widget.on_new_game)
        self.ui.rental_agency.triggered.connect(self.widget.rent_house)
        self.ui.beijing_intro.triggered.connect(self.beijing_intro)
        self.ui.game_help.triggered.connect(self.game_doc)
        self.ui.story.triggered.connect(self.show_story)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check)
        # self.timer.start()

    def show_story(self):
        from widgets.story import StoryDlg

        self.d_story = StoryDlg(c_continue=True)
        self.d_story.show()

    def game_doc(self):
        import webbrowser

        webbrowser.open(self.widget.d_story.help_file)

    def beijing_intro(self):
        self.intro = BeijingIntro()
        self.intro.show()

    def set_title(self, time_left: int):
        self.setWindowTitle(
            self.tr("Beijing Life ({}/{} day)").format(40 - time_left, 40)
        )

    def check(self):
        from pathlib import Path

        CURRENT = Path(__file__).resolve().parent
        reload_action = CURRENT.parent.joinpath("ui/_reload")

        self.app.removeTranslator(self.translator)
        self.translator.load("translation_zh_CN.qm")
        self.app.installTranslator(self.translator)

        if reload_action.exists():
            reload_action.unlink()
            import importlib

            importlib.reload(main_widget)
            importlib.reload(ui.main_widget)
            self.widget.setParent(None)
            self.widget = main_widget.MainWidget()
            self.setCentralWidget(self.widget)
