from PySide6 import QtWidgets, QtGui, QtCore, QtMultimedia
import random
from app.models import makeDrugPrices, get_item_name, Item
from widgets.my_table_model import MyTableModel
from ui.main import Ui_MainWindow

from widgets import (
    AboutGame,
    Bank,
    Airport,
    CyberCafe,
    Diary,
    Settings,
    StoryDlg,
    TextEditor,
    Hospital,
    PayDebt,
    Buy,
    Sell,
)


from app.models import Status
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
            QLabel, QPushButton, QTextBrowser, QGroupBox, QTextEdit, QRadioButton {{
                font: 12pt {family};
            }}
            """.format(family=family)
        )
        self.ui.menubar.setFont(QtGui.QFont(family, 14))
        self.ui.menu.setFont(QtGui.QFont(family, 14))
        self.ui.menu_2.setFont(QtGui.QFont(family, 14))
        self.ui.menu_3.setFont(QtGui.QFont(family, 14))
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
        self.n_cafe = 0
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

        self.places: list[QtWidgets.QPushButton] = [
            getattr(self.ui, f"x{i}") for i in range(10)
        ]
        for i in range(len(self.places)):
            self.places[i].clicked.connect(self.getaction(i))

        self.in_subway = True
        self.ui.switch_place.clicked.connect(self.switch_place)
        self.ui.switch_mode.clicked.connect(self.switch_mode)

        self.ui.bank.triggered.connect(self.enter_bank)
        self.ui.p_bank.clicked.connect(self.enter_bank)
        self.ui.hospital.triggered.connect(self.enter_hospital)
        self.ui.p_hospital.clicked.connect(self.enter_hospital)

        self.ui.post_office.triggered.connect(self.pay_debt)
        self.ui.p_postoffice.clicked.connect(self.pay_debt)

        self.init_data()
        self.refresh_display()
        self.indexes = []
        self.sell_indexes = []

    def black_market_items(self, selected, deselected):
        if len(selected.indexes()) == 0:
            self.indexes = []
        else:
            self.indexes = [index.row() for index in selected.indexes()]

    def my_home_items(self, selected, deselected):
        if len(selected.indexes()) == 0:
            self.sell_indexes = []
        else:
            self.sell_indexes = [index.row() for index in selected.indexes()]

    def pay_debt(self):
        if self.status.debt > 0:
            self.d_paydebt = PayDebt(self.status.cash, self.status.debt)
            self.d_paydebt.sig_pay.connect(self.after_pay_debt)
            self.d_paydebt.show()
        else:
            amount = self.status.cash + self.status.saving
            if amount < 1000:
                self.d_diary = Diary()
                self.d_diary.ui.label.setText(
                    self.tr(
                        'The village chief laughed and said: "You have no money, you are crazy!"'
                    )
                )
                self.d_diary.show()
            elif 1000 < amount < 100000:
                self.d_diary = Diary()
                self.d_diary.ui.label.setText(
                    self.tr(
                        'The village chief nodded to me: "Brother, do you want to support your hometown with 1,000 yuan?"'
                    )
                )
                self.d_diary.show()
            elif 100000 < amount < 10000000:
                self.d_diary = Diary()
                self.d_diary.ui.label.setText(
                    self.tr(
                        'The village chief bowed to me on the phone: "Rich man! I want to marry my daughter to you."...'
                    )
                )
                self.d_diary.show()
            elif amount > 10000000:
                self.d_diary = Diary()
                self.d_diary.ui.label.setText(
                    self.tr(
                        'The village chief knelt down to me on the phone and said: "You are my real father!"'
                    )
                )
                self.d_diary.show()
            else:
                self.d_diary = Diary()
                self.d_diary.ui.label.setText(
                    self.tr(
                        'The village chief said: "You are a role model for rural young people!"'
                    )
                )
                self.d_diary.show()

    def after_pay_debt(self, cash, debt):
        self.status.cash = cash
        self.status.debt = debt
        self.refresh_display()

    def enter_hospital(self):
        if self.status.health == 100:
            self.d_diary = Diary()
            self.d_diary.ui.label.setText(
                self.tr(
                    'The young nurse looked at me with a smile and said, "Brother! Please register at the neurology department."'
                )
            )
            self.d_diary.show()
        else:
            self.d_hospital = Hospital(None, self.status.cash, self.status.health)
            self.d_hospital.sig_health.connect(self.leave_hospital)
            self.d_hospital.show()

    def leave_hospital(self, cash: int, health: int):
        self.status.cash = cash
        self.status.health = health
        self.refresh_display()

    def enter_bank(self):
        self.d_bank = Bank(None, self.status.cash, self.status.saving)
        self.d_bank.sig_account.connect(self.leave_bank)
        self.d_bank.show()

    def leave_bank(self, cash, saving):
        self.status.cash = cash
        self.status.saving = saving
        self.refresh_display()

    def switch_mode(self):
        self.text_editor = TextEditor()
        self.text_editor.show()

    def switch_place(self):
        self.in_subway = not self.in_subway
        self.texts_subway = [
            self.tr("Beijing Railway \nStation"),
            self.tr("Pingguoyuan"),
            self.tr("Gongzhufen"),
            self.tr("Xizhimen"),
            self.tr("Jishuitan"),
            self.tr("Dongzhimen"),
            self.tr("Fuxingmen"),
            self.tr("Jianguomen"),
            self.tr("Changchun Street"),
            self.tr("Chongwenmen"),
        ]
        self.texts_city = [
            self.tr("Fangzhuang"),
            self.tr("Bajiao West Road"),
            self.tr("Cuiwei Road"),
            self.tr("Haidian Street"),
            self.tr("Asian Games Village"),
            self.tr("Sanyuan West Bridge"),
            self.tr("Fuyou Street"),
            self.tr("Yong'anli"),
            self.tr("Yuquanying"),
            self.tr("Yongdingmen"),
        ]
        for i in self.places:
            i.setDisabled(False)
        if self.in_subway:
            self.ui.switch_place.setText(self.tr("I want to visit \nthe capital"))
            for i in range(len(self.places)):
                self.places[i].setText(self.texts_subway[i])
        else:
            self.ui.switch_place.setText(self.tr("I want to go\n to the subway"))
            for i in range(len(self.places)):
                self.places[i].setText(self.texts_city[i])

    def getaction(self, btn_number: int):
        def action():
            for i in self.places:
                i.setDisabled(False)
            self.places[btn_number].setDisabled(True)

        return action

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
        self.quantity = 0
        status, market_items, my_items = load_data()
        self.status: Status = status

        self.market_items: list[Item] = makeDrugPrices(3)
        self.my_items: list[Item] = my_items

        font = QtGui.QFont("MiSans", 12)
        self.model_market = MyTableModel()
        self.ui.black_market.setModel(self.model_market)
        self.ui.black_market.setFont(font)

        self.model_myitem = MyTableModel()
        self.ui.my_room.setModel(self.model_myitem)
        self.ui.my_room.setFont(font)

        self.ui.black_market.selectionModel().selectionChanged.connect(
            self.black_market_items
        )
        self.ui.my_room.selectionModel().selectionChanged.connect(self.my_home_items)

        self.quantity = sum([x.quantity for x in self.my_items])

    def play_sound(self, name: str):
        # the "self" is important because sound will run in the background
        self.effect = QtMultimedia.QSoundEffect()
        self.effect.setSource(QtCore.QUrl.fromLocalFile(f":/SND/sound/{name}"))
        self.effect.setLoopCount(1)
        self.effect.setVolume(0.8)
        self.effect.play()

    def buy(self):
        if len(self.indexes) == 0:
            self.dialog = Diary()
            self.dialog.ui.label.setText(self.tr("I haven't decided what to buy yet."))
            self.dialog.show()
        else:
            item = self.market_items[self.indexes[0]]
            if self.status.cash < item.price:
                if self.status.saving > 0:
                    self.dialog = Diary()
                    self.dialog.ui.label.setText(
                        self.tr(
                            "I don't have enough cash with me, so I'll go to the bank to withdraw some money."
                        )
                    )
                    self.dialog.show()
                else:
                    self.dialog = Diary()
                    self.dialog.ui.label.setText(
                        self.tr(
                            "I don't have enough cash and I don't have any deposits in the bank, what should I do?"
                        )
                    )
                    self.dialog.show()
            else:
                self.d_buy = Buy(
                    self.status.cash,
                    self.market_items[self.indexes[0]],
                    self.quantity == 100,
                )
                self.d_buy.ui.pushButton.clicked.connect(self.finish_buy)
                self.d_buy.show()

    def finish_buy(self):
        self.play_sound("buy.wav")
        buy_amount = self.d_buy.ui.spinBox.value()
        self.status.cash -= self.d_buy.item.price * buy_amount
        item = self.d_buy.item
        item.quantity = buy_amount
        self.my_items.append(item)
        self.refresh_display()

    def sell(self):
        if len(self.sell_indexes) == 0:
            pass
        else:
            self.d_sell = Sell(self.my_items[self.sell_indexes[0]])
            self.d_sell.ui.pushButton.clicked.connect(self.finish_sell)
            self.d_sell.show()

    def get_price(self, item: Item):
        names = [x.name for x in self.market_items]
        if item.name in names:
            index = names.index(item.name)
            market_item = self.market_items[index]
            return market_item.price
        else:
            return -1

    def finish_sell(self):
        self.play_sound("money.wav")
        quantity = self.d_sell.ui.spinBox.value()
        price = self.get_price(self.d_sell.item)
        if price == -1:
            self.d_diary = Diary()
            self.d_diary.ui.label.setText(
                self.tr("Oh? It seems that no one is doing {} business here.").format(
                    get_item_name(self.d_sell.item)
                )
            )
            self.d_diary.show()
        else:
            self.status.cash += quantity * self.get_price(self.d_sell.item)
            names = [x.name for x in self.my_items]
            index = names.index(self.d_sell.item.name)
            self.my_items[index].quantity -= quantity
            if self.my_items[index].quantity == 0:
                del self.my_items[index]
            self.refresh_display()

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
        if self.status.cash < 15:
            self.d_diary = Diary()
            self.d_diary.ui.label.setText(
                self.tr(
                    "You need to bring at least 15 yuan with you when entering an Internet cafe, haha, come back after withdrawing money."
                )
            )
            self.d_diary.show()
        elif self.n_cafe > 2:
            self.d_diary = Diary()
            self.d_diary.ui.label.setText(
                self.tr(
                    "The village chief said: Don't hang out in the Internet cafe all the time, go and do a decent business!"
                )
            )
            self.d_diary.show()
        else:
            self.n_cafe += 1
            self.cafe = CyberCafe()
            self.cafe.ui.leave_cybercafe.clicked.connect(self.finish_cyber_cafe)
            self.cafe.show()

    def finish_cyber_cafe(self):
        money = random.randint(1, 10)
        self.status.cash += money
        self.refresh_display()

        self.d_diary = Diary()
        self.d_diary.ui.label.setText(
            self.tr(
                "Thanks to the telecommunications reform, you can surf the Internet for free! And I also earned {} yuan in US Internet advertising fees, hehe!"
            ).format(money)
        )
        self.d_diary.show()

    def refresh_display(self):
        self.ui.cash.display(self.status.cash)
        self.ui.saving.display(self.status.saving)
        self.ui.fame.display(self.status.fame)
        self.ui.debt.display(self.status.debt)
        self.ui.health.display(self.status.health)

        self.model_market.clear()
        for item in self.market_items:
            name = QtGui.QStandardItem(get_item_name(item))
            icon = QtGui.QIcon(":/res/item.ico")
            name.setIcon(icon)
            price = QtGui.QStandardItem(str(item.price))
            self.model_market.appendRow([name, price])

        self.model_market.setHorizontalHeaderLabels(
            [self.tr("Goods"), self.tr("Black Market prices")]
        )

        header = self.ui.black_market.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.ui.black_market.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.ui.black_market.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.model_myitem.clear()
        for item in self.my_items:
            name = QtGui.QStandardItem(get_item_name(item))
            icon = QtGui.QIcon(":/res/item.ico")
            name.setIcon(icon)
            price = QtGui.QStandardItem(str(item.price))
            quantity = QtGui.QStandardItem(str(item.quantity))
            self.model_myitem.appendRow([name, price, quantity])

        self.model_myitem.setHorizontalHeaderLabels(
            [self.tr("Goods"), self.tr("Bought price"), self.tr("Quantity")]
        )

        header = self.ui.my_room.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.ui.my_room.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
        self.ui.my_room.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

    def show_intro(self):
        self.dlg = StoryDlg()
        self.dlg.start_sig.connect(self.check_start)
        self.dlg.show()

    def check_start(self):
        self.show()
