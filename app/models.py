from dataclasses import dataclass

from enum import Enum, auto

@dataclass
class Status:
    cash: int = 2000
    saving: int = 0
    debt: int = 5000
    health: int = 100
    fame: int = 100


class ItemName(Enum):
    cigar = 0
    car = auto()
    vcd_game = auto()
    liquor = auto()
    r18_book = auto()
    toys = auto()
    makeup = auto()
    phone = auto()


@dataclass
class Item:
    name: ItemName = ItemName.car
    price: int = 0

