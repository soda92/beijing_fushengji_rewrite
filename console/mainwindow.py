from app.models import Status, Item, ItemName
from PySide6 import QtCore
import sys


class MainWindow(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def print_items(self, items: list[Item]):
        if len(items) == 0:
            print("None")
        tr = self.tr
        for item in items:
            print(tr("name"), end=":")
            if item.name == ItemName.car:
                print(tr("smuggled cars"))
            elif item.name == ItemName.cigar:
                print(tr("imported cigarettes"))
            elif item.name == ItemName.vcd_game:
                print(tr("Pirated VCDs and games"))
            elif item.name == ItemName.r18_book:
                print(tr("Shanghai baby (r18)"))
            elif item.name == ItemName.toys:
                print(tr("imported toys"))
            elif item.name == ItemName.makeup:
                print(tr("Fake cosmetics"))
            print(tr("price"), ":", item.price)


    def print_market(self, items: list[Item]):
        print(self.tr("black market"))
        self.print_items(items)


    def print_my_items(self, items: list[Item]):
        print(self.tr("my items"))
        self.print_items(items)


    def print_status(self, status: Status):
        print(self.tr("cash"), status.cash)
        print(self.tr("saving"), status.saving)
        print(self.tr("debt"), status.debt)
        print(self.tr("health"), status.health)
        print(self.tr("fame"), status.fame)


    def start(self, status: Status, market_items: list[Item], my_items: list[Item]):
        self.status = status
        self.market_items = market_items
        self.my_items = my_items

        while True:
            self.print_market(self.market_items)
            self.print_my_items(self.my_items)
            self.print_status(self.status)

            print("Please choose: &Buy, &Sell, &Hospital, &Rent, &Net, &Post_office, Ban&k")
            print("Please choose: about_&beijing, &story, &doc, &intro, &about")
            print("Please choose: ne&ws, &tour_subway, tour_&city, switch_&mode")
            action = input("Please choose: &new_game, &ranking, se&tting, &exit\n")

            self.process_action(action)

    def process_action(self, action: str):
        if action == "e":
                sys.exit(0)


def main():
    status = Status()
    market_items = []
    my_items = []

    app = QtCore.QCoreApplication(sys.argv)
    window = MainWindow()
    window.start(status, market_items, my_items)
    sys.exit(app.exec())
