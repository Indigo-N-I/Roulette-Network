from enum import Enum

class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class BetType(OrderedEnum):
    # 1:1 bets
    PARITY = 0
    COLOR = 1
    HIGH_LOW = 2

    # 2:1 bets
    COLUMN = 3
    DOZEN = 4
    SNAKE = 5

    # 5:1 BETS
    LINE = 6

    # 6:1 BETS
    FIVE_NUM = 7
    BASKET = 8

    # 8:1 BETS
    CORNER = 9

    # 11:1 BETS
    STREET = 10

    # 17:1 BETS
    SPLIT = 11

    # 35:1 BETS
    STRAIGHT_UP = 12

class Bet():
    def __init__(self, money, bet_type: BetType, wins):
        self.wager = money
        self.type = bet_type
        self.wins = wins

        self.check_valid()


    def check_valid(self):
        if self.type < BetType.COLUMN:
            assert len(self.wins) <= 18, f"{self.type} cannot have wins of {self.wins}"
        elif self.type < BetType.LINE:
            assert len(self.wins) <= 12, f'{self.type} cannot have wins of {self.wins}'
        elif self.type < BetType.FIVE_NUM:
            assert len(self.wins) == 6, f'{self.type} cannot have wins of {self.wins}'
        elif self.type < BetType.CORNER:
            assert len(self.wins) == 4 or len(self.wins) == 4, f'{self.type} cannot have wins of {self.wins}'
        elif self.type < BetType.STREET:
            assert len(self.wins) == 4, f'{self.type} cannot have wins of {self.wins}'
        elif self.type < BetType.SPLIT:
            assert len(self.wins) == 3, f'{self.type} cannot have wins of {self.wins}'
        elif self.type < BetType.STRAIGHT_UP:
            assert len(self.wins) == 2, f'{self.type} cannot have wins of {self.wins}'
        else:
            assert len(self.wins) == 1, f'{self.type} cannot have wins of {self.wins}'

    def __str__(self):
        return f"${self.wager} {self.type} bet with wins on {self.wins}"

    def __repr__(self):
        return f'bets.Bet({self.wager}, {self.type}, {self.wins})'

    def get_bet(self):
        return self.wager
