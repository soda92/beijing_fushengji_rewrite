from PySide6 import QtWidgets, QtGui, QtCore, QtMultimedia
import random
from app.models import makeDrugPrices, get_item_name, Item, ItemName
from ui.main import Ui_MainWindow
from widgets.tables import BlackMarketTable, MyItemsTable

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
    News,
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
                self.show_diary(
                    self.tr(
                        'The village chief laughed and said: "You have no money, you are crazy!"'
                    )
                )
            elif 1000 < amount < 100000:
                self.show_diary(
                    self.tr(
                        'The village chief nodded to me: "Brother, do you want to support your hometown with 1,000 yuan?"'
                    )
                )
            elif 100000 < amount < 10000000:
                self.show_diary(
                    self.tr(
                        'The village chief bowed to me on the phone: "Rich man! I want to marry my daughter to you."...'
                    )
                )
            elif amount > 10000000:
                self.show_diary(
                    self.tr(
                        'The village chief knelt down to me on the phone and said: "You are my real father!"'
                    )
                )
            else:
                self.show_diary(
                    self.tr(
                        'The village chief said: "You are a role model for rural young people!"'
                    )
                )

    def after_pay_debt(self, cash, debt):
        self.status.cash = cash
        self.status.debt = debt
        self.refresh_display()

    def show_diary(self, text: str):
        self.d_diary = Diary()
        self.d_diary.ui.label.setText(text)
        self.d_diary.exec()

    def show_news(self, text: str):
        self.d_diary = News()
        self.d_diary.ui.label.setText(text)
        self.d_diary.exec()

    def enter_hospital(self):
        if self.status.health == 100:
            self.show_diary(
                self.tr(
                    'The young nurse looked at me with a smile and said, "Brother! Please register at the neurology department."'
                )
            )
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
            self.handle_normal_events()

        return action

    def show_settings(self):
        self.d_settings = Settings(None, self.allow_hacker, self.turn_off_sound)
        self.d_settings.show()
        self.d_settings.sig_settings.connect(self.settings)

    def go_airport(self):
        self.d_airport = Airport()
        self.d_airport.show()

    def show_about(self):
        self.about_game = AboutGame()
        self.about_game.show()

    def settings(self, allow_hacker: bool, turn_off_sound: bool):
        self.turn_off_sound = turn_off_sound
        self.allow_hacker = allow_hacker

    def init_data(self):
        self.enable_help = False
        self.turn_off_sound = False
        self.allow_hacker = False
        self.quantity = 0
        self.max_quantity = 100
        status, market_items, my_items = load_data()
        self.status: Status = status

        self.market_items: list[Item] = makeDrugPrices(3)
        self.my_items: list[Item] = my_items

        self.t_1 = BlackMarketTable(self.ui.black_market)
        self.t_2 = MyItemsTable(self.ui.my_room)

        self.ui.black_market.selectionModel().selectionChanged.connect(
            self.black_market_items
        )
        self.ui.my_room.selectionModel().selectionChanged.connect(self.my_home_items)

        self.quantity = sum([x.quantity for x in self.my_items])

        self.time_left = 40

    def handle_cash_and_debt(self):
        self.status.debt *= 1.1
        self.status.saving *= 1.01

        self.status.debt = int(self.status.debt)
        self.status.saving = int(self.status.saving)

    def handle_normal_events(self):
        if self.time_left <= 2:
            self.market_items = makeDrugPrices(0)
        else:
            self.market_items = makeDrugPrices(3)
        self.handle_cash_and_debt()
        self.do_random_stuff()
        self.do_random_event()
        self.on_steal()

        self.time_left -= 1
        self.setWindowTitle(
            self.tr("Beijing Life ({}/{} day)").format(40 - self.time_left, 40)
        )

        if self.time_left == 1:
            self.show_diary(
                self.tr(
                    "I'm going back to my hometown tomorrow and selling all the goods quickly."
                )
            )
        if self.time_left == 0:
            self.show_diary(
                self.tr(
                    "I have been in Beijing for 40 days, it’s time to go back and get married."
                )
            )
            if len(self.my_items) != 0:
                self.show_diary(
                    self.tr("The system sold the remaining goods for me: {}").format(
                        ",".join(list(map(get_item_name, self.my_items)))
                    )
                )
                for i in self.my_items:
                    self.status.cash += self.get_price(i) * i.quantity
                self.my_items = []
            self.on_exit()

        self.refresh_display()

    def do_random_event(self):
        pass

    def do_random_stuff(self):
        from dataclasses import dataclass

        @dataclass
        class GameMessage:
            freq: int
            msg: str
            drug: ItemName
            plus: int
            minus: int
            add: int

        gameMessages = [
            [
                170,
                MainWindow.tr(
                    'Experts propose to improve college students\' "hands-on quality", imported toys are popular!'
                ),
                ItemName.toys,
                2,
                0,
                0,
            ],
            [
                139,
                MainWindow.tr(
                    "Some people proudly say: When you are sick, you don't need to take injections or medicine, just drink fake liquor (very toxic)!"
                ),
                ItemName.liquor,
                3,
                0,
                0,
            ],
            [
                100,
                MainWindow.tr(
                    'Hospital\'s secret report: "Shanghai Baby" is more effective than Viagra"!'
                ),
                ItemName.r18_book,
                5,
                0,
                0,
            ],
            [
                41,
                MainWindow.tr(
                    'The illiterate said: "2000 Nobel Prize in Literature? Bah! Not as good as pirated VCD Hong Kong and Taiwan movies." ”'
                ),
                ItemName.vcd_game,
                4,
                0,
                0,
            ],
            [
                37,
                MainWindow.tr(
                    'Editorial of "Beijing Economic Newspaper": "Smuggling cars vigorously promotes car consumption!"'
                ),
                ItemName.car,
                3,
                0,
                0,
            ],
            [
                23,
                MainWindow.tr(
                    'Editorial of "Beijing Truth": "Promote beauty and put it into practice", counterfeit cosmetics are very popular!'
                ),
                ItemName.makeup,
                4,
                0,
                0,
            ],
            [
                37,
                MainWindow.tr(
                    '8858.com e-bookstore dare not sell "Shanghai Baby", a copy can be sold at a sky-high price on the black market!'
                ),
                ItemName.r18_book,
                8,
                0,
                0,
            ],
            [
                15,
                MainWindow.tr(
                    'Xie Bufeng said at the party: "I am cool! I use counterfeit cosmetics!", counterfeit cosmetics are in short supply!'
                ),
                ItemName.makeup,
                7,
                0,
                0,
            ],
            [
                40,
                MainWindow.tr(
                    "Some people in Beijing drink fake Shanxi wine crazily, and can sell it at a sky-high price!"
                ),
                ItemName.liquor,
                7,
                0,
                0,
            ],
            [
                29,
                MainWindow.tr(
                    "College students in Beijing start looking for jobs, parallel-imported mobile phones are very popular!!"
                ),
                ItemName.phone,
                7,
                0,
                0,
            ],
            [
                35,
                MainWindow.tr(
                    "Rich people in Beijing are crazy about buying smuggled cars! Prices are soaring!"
                ),
                ItemName.car,
                8,
                0,
                0,
            ],
            [
                17,
                MainWindow.tr(
                    "The market is flooded with smuggled cigarettes from Fujian!"
                ),
                ItemName.cigar,
                0,
                8,
                0,
            ],
            [
                24,
                MainWindow.tr(
                    "Children in Beijing are busy studying online, no one wants to buy imported toys."
                ),
                ItemName.toys,
                0,
                5,
                0,
            ],
            [
                18,
                MainWindow.tr(
                    'The piracy industry is booming, and Zhongguancun, the "Silicon Valley of China", is full of village girls selling pirated VCDs!'
                ),
                ItemName.vcd_game,
                0,
                8,
                0,
            ],
            [
                160,
                MainWindow.tr(
                    "My old classmate in Xiamen sponsored me two smuggled cars! I'm rich!"
                ),
                ItemName.car,
                0,
                0,
                2,
            ],
            [
                45,
                MainWindow.tr(
                    "After the Industrial and Commercial Bureau raided the place, I found the imported cigarettes lost by my fellow villager in a dark corner."
                ),
                ItemName.cigar,
                0,
                0,
                6,
            ],
            [
                35,
                MainWindow.tr(
                    "My fellow villager gave me some fake Shanxi liquor (highly toxic) before he went home!"
                ),
                ItemName.liquor,
                0,
                0,
                4,
            ],
            [
                140,
                MainWindow.tr(
                    "Media reports: Another Japanese product exported to China has gone wrong! After the incident, the Japanese refused to admit it and refused to compensate. The village chief learned of this news and asked someone to sell you his parallel-imported mobile phone (without any manufacturer logo) for 2,500 yuan."
                ),
                ItemName.phone,
                0,
                0,
                1,
            ],
        ]
        messages: list[GameMessage] = []
        for i in gameMessages:
            m = GameMessage(*i)
            # m.freq, m.msg, m.drug, m.plus, m.minus, m.add = i
            messages.append(m)

        for k, message in enumerate(messages):
            r = random.randint(0, 950)

            if r % message.freq == 0:
                if message.drug not in [x.name for x in self.market_items]:
                    continue
                index = [x.name for x in self.market_items].index(message.drug)

                self.show_news(message.msg)
                if k == len(messages) - 1:
                    self.status.debt += 2500

                # price multipled
                if message.plus > 0:
                    self.market_items[index].price *= message.plus
                # price divided
                if message.minus > 0:
                    self.market_items[index].price /= message.minus
                    self.market_items[index].price = int(self.market_items[index].price)

                if message.add > 0:
                    max_add_count = self.max_quantity - self.quantity
                    add_count = message.add
                    if add_count > max_add_count:
                        add_count = max_add_count
                    if add_count == 0:
                        self.show_diary(
                            self.tr(
                                "What a pity! The house I rented is too small and can only hold {} items."
                            ).format(self.max_quantity)
                        )
                    else:
                        item = Item()
                        item.name = message.drug
                        item.price = 0
                        item.quantity = add_count
                        if k == len(messages) - 1:
                            item.price = 2500

                        if item.name not in [x.name for x in self.my_items]:
                            self.my_items.append(item)
                        else:
                            index = [x.name for x in self.my_items].index(item.name)
                            self.my_items[index].quantity += add_count

        self.refresh_display()

    def on_steal(self):
        pass

    def on_exit(self):
        pass

    def play_sound(self, name: str):
        if not self.turn_off_sound:
            # the "self" is important because sound will run in the background
            self.effect = QtMultimedia.QSoundEffect()
            self.effect.setSource(QtCore.QUrl.fromLocalFile(f":/SND/sound/{name}"))
            self.effect.setLoopCount(1)
            self.effect.setVolume(0.8)
            self.effect.play()

    def buy(self):
        if len(self.indexes) == 0:
            self.show_diary(self.tr("I haven't decided what to buy yet."))
        else:
            item = self.market_items[self.indexes[0]]
            if self.status.cash < item.price:
                if self.status.saving > 0:
                    self.show_diary(
                        self.tr(
                            "I don't have enough cash with me, so I'll go to the bank to withdraw some money."
                        )
                    )
                else:
                    self.show_diary(
                        self.tr(
                            "I don't have enough cash and I don't have any deposits in the bank, what should I do?"
                        )
                    )
            else:
                self.d_buy = Buy(
                    self.status.cash,
                    self.market_items[self.indexes[0]],
                    self.quantity,
                    self.max_quantity,
                )
                self.d_buy.ui.pushButton.clicked.connect(self.finish_buy)
                self.d_buy.show()

    def finish_buy(self):
        buy_amount = self.d_buy.ui.spinBox.value()
        if buy_amount != 0:
            self.play_sound("buy.wav")
            self.status.cash -= self.d_buy.item.price * buy_amount
            item = self.d_buy.item
            item.quantity = buy_amount
            self.my_items.append(item)
            self.refresh_display()

    def sell(self):
        if len(self.sell_indexes) == 0:
            pass
        else:
            item = self.my_items[self.sell_indexes[0]]
            price = self.get_price(item)
            if price == -1:
                self.show_diary(
                    self.tr(
                        "Oh? It seems that no one is doing {} business here."
                    ).format(get_item_name(item))
                )
            else:
                self.d_sell = Sell(item)
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
            self.show_diary(
                self.tr(
                    "You need to bring at least 15 yuan with you when entering an Internet cafe, haha, come back after withdrawing money."
                )
            )
        elif self.n_cafe > 2:
            self.show_diary(
                self.tr(
                    "The village chief said: Don't hang out in the Internet cafe all the time, go and do a decent business!"
                )
            )
        else:
            self.n_cafe += 1
            self.cafe = CyberCafe()
            self.cafe.ui.leave_cybercafe.clicked.connect(self.finish_cyber_cafe)
            self.cafe.show()

    def finish_cyber_cafe(self):
        money = random.randint(1, 10)
        self.status.cash += money
        self.refresh_display()

        self.show_diary(
            self.tr(
                "Thanks to the telecommunications reform, you can surf the Internet for free! And I also earned {} yuan in US Internet advertising fees, hehe!"
            ).format(money)
        )

    def refresh_display(self):
        self.ui.cash.display(self.status.cash)
        self.ui.saving.display(self.status.saving)
        self.ui.fame.display(self.status.fame)
        self.ui.debt.display(self.status.debt)
        self.ui.health.display(self.status.health)

        self.t_1.slot_items(self.market_items)
        self.t_2.slot_items(self.my_items)

        self.quantity = sum([x.quantity for x in self.my_items])
        self.ui.label_7.setText(
            self.tr("your rented house ({}/{})").format(
                self.quantity, self.max_quantity
            )
        )


    def show_intro(self):
        self.dlg = StoryDlg()
        self.dlg.start_sig.connect(self.check_start)
        self.dlg.show()

    def check_start(self):
        self.show()
