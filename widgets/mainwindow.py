from PySide6 import QtWidgets, QtGui, QtCore
import ui.mainwindow as ui_mainwindow
import ui.main_widget
import main_rc
import widgets.main_widget as main_widget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.ui = ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.widget = main_widget.MainWidget()
        self.setCentralWidget(self.widget)

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
        self.ui.cybercafe.triggered.connect(self.widget.enter_cafe)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.check)
        self.timer.start()

    def check(self):
        from pathlib import Path

        CURRENT = Path(__file__).resolve().parent
        reload_action = CURRENT.parent.joinpath("ui/_reload")
        if reload_action.exists():
            reload_action.unlink()
            import importlib

            importlib.reload(main_widget)
            importlib.reload(ui.main_widget)
            importlib.reload(main_rc)
            self.widget.setParent(None)
            self.widget = main_widget.MainWidget()
            self.setCentralWidget(self.widget)
