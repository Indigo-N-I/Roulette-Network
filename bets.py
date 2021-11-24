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
    PARITY = 0 # even or odd
    COLOR = 1 # red or black
    HIGH_LOW = 2 # high or low

    # 2:1 bets
    COLUMN = 3 # 1's 2's 3's
    DOZEN = 4 # 1-12, 13-24, 25-36
    SNAKE = 5 # 1, 5, 9, 12, 14, 16,19, 23, 27, 30, 32, 34

    # 5:1 BETS
    LINE = 6 # factors of 3

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


PARITY_BETS = [[i for i in range(1,37) if i %2 == 0], [i for i in range(1,37) if i %2 == 1]]
PARITY_BETS_ENUM = [BetType.PARITY for i in PARITY_BETS]
COLOR_BETS = [[1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36], [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]]
COLOR_BETS_ENUM = [BetType.COLOR for i in COLOR_BETS]
HIGH_LOW_BETS = [[i for i in range(1,19)], [i for i in range(19, 37)]]
HIGH_LOW_BETS_ENUM = [BetType.HIGH_LOW for i in HIGH_LOW_BETS]

COLUMN_BETS = [[i for i in range(1,37) if i %3 == 1], [i for i in range(1,37) if i %3 == 2], [i for i in range(1,37) if i %3 == 0]]
COLUMN_BETS_ENUM = [BetType.COLUMN for i in COLUMN_BETS]
DOZEN_BETS = [[i for i in range(1,13)], [i for i in range(13, 25)], [i for i in range(25,37)]]
DOZEN_BETS_ENUM = [BetType.DOZEN for i in DOZEN_BETS]
SNAKE_BET = [[1, 5, 9, 12, 14, 16, 19, 23, 27, 30, 32, 34]]
SNAKE_BET_ENUM = [BetType.SNAKE for i in SNAKE_BET]

LINE_BETS = [[i for i in range(a*3+1, a*3 + 7)] for a in range(11)]
LINE_BETS_ENUM = [BetType.LINE for i in LINE_BETS]

BASKET_BET = [[-1, 0, 1, 2, 3]]
BASKET_BET_ENUM = [BetType.BASKET for i in BASKET_BET]

CORNER_BETS = [[i for i in range(b, b + 2)] + [i for i in range(b + 3, b + 5)] for b in range(33) if b % 3 != 0]
CORNER_BETS_ENUM = [BetType.CORNER for i in CORNER_BETS]

STREET_BETS = [[i for i in range(a*3+1, a*3 + 4)] for a in range(12)]
STREET_BETS_ENUM = [BetType.STREET for i in STREET_BETS]

SPLIT_BETS = [[b, b + 1] for b in range(37) if b % 3 != 0]
SPLIT_BETS += [[b, b + 3] for b in range(1, 34)]
SPLIT_BETS += [[-1,0], [0,1], [0,2], [-1,2], [-1,3]]
SPLIT_BETS_ENUM = [BetType.SPLIT for i in SPLIT_BETS]

STRAIGHT_UP_BETS = [[i] for i in range(-1,37)]
STRAIGHT_UP_BETS_ENUM = [BetType.STRAIGHT_UP for i in STRAIGHT_UP_BETS]

ALL_BETS = PARITY_BETS + COLOR_BETS + HIGH_LOW_BETS + COLUMN_BETS + DOZEN_BETS + SNAKE_BET + LINE_BETS + BASKET_BET + CORNER_BETS + STREET_BETS + SPLIT_BETS + STRAIGHT_UP_BETS
ALL_BETS_ENUM = PARITY_BETS_ENUM + COLOR_BETS_ENUM + HIGH_LOW_BETS_ENUM + COLUMN_BETS_ENUM + DOZEN_BETS_ENUM + SNAKE_BET_ENUM \
                + LINE_BETS_ENUM + BASKET_BET_ENUM + CORNER_BETS_ENUM + STREET_BETS_ENUM + SPLIT_BETS_ENUM + STRAIGHT_UP_BETS_ENUM
# print(len(ALL_BETS_ENUM))


class Bet():
    def __init__(self, money, BetType: BetType, wins):
        self.wager = money
        self.type = BetType
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
            assert len(self.wins) == 5 or len(self.wins) == 4, f'{self.type} cannot have wins of {self.wins}'
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

    def get_type(self):
        return self.type
