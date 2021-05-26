from abc import ABC, abstractmethod
import random
from bets import Bet, BetType

class Player(ABC):

    def __init__(self, start_money = 1000):
        self.money = start_money
        self.history = []
        self.bets = []
        self.max_money = start_money
        super().__init__()

    @abstractmethod
    def make_bets(self):
        pass

    def amount_bet(self):
        return sum([bet.get_bet() for bet in self.history])

    def rounds_bet(self):
        return len(self.history)

    def wins(self, money):
        self.money += money
        if self.money > self.max_money:
            self.max_money = self.money

    def can_bet(self, amount):
        return amount < self.money

    def can_play(self):
        return self.money > 0

    def max_bet(self):
        return self.money

    def clear_bet(self):
        self.bets = []

    def get_bets(self):
        return self.bets

    def get_max_money(self):
        return self.max_money

class ColorBetter(Player):
    def __init__(self, start_money = 1000, bet_amount = 100):
        self.bet_amount = bet_amount
        super().__init__(start_money)

    def make_bets(self):
        red = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        black = [i for i in range(1,37) if i not in red]

        if self.can_bet(self.bet_amount):
            self.money -= self.bet_amount
            if random.randint(0,1):
                outcome = Bet(self.bet_amount, BetType.COLOR, red)
                self.bets.append(outcome)
            else:
                outcome = Bet(self.bet_amount, BetType.COLOR, black)
                self.bets.append(outcome)
        else:
            betting = self.max_bet()
            self.money -= betting
            if random.randint(0,1):
                outcome = Bet(betting, BetType.COLOR, red)
                self.bets.append(outcome)
            else:
                outcome = Bet(betting, BetType.COLOR, black)
                self.bets.append(outcome)

        self.history.append(self.bets)
        return outcome

if __name__ == '__main__':
    a = ColorBetter()
    a.make_bets()
