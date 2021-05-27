import random
from bets import BetType, ALL_BETS
import numpy as np

class Roulette():
    def __init__(self, double_zeros = True):
        self.vals = [i - int(double_zeros) for i in range(38 - int(double_zeros))]
        self.prev_rounds = []

    def spin(self):
        return random.choice(self.vals)

    def pay_out(self, bet, value):
        spin = value
        if spin in bet.wins:
            if bet.type < BetType.COLUMN:
                return 2*bet.wager
            elif bet.type < BetType.LINE:
                return 3* bet.wager
            elif bet.type < BetType.FIVE_NUM:
                return 6 * bet.wager
            elif bet.type < BetType.CORNER:
                return 7 * bet.wager
            elif bet.type < BetType.STREET:
                return 9 * bet.wager
            elif bet.type < BetType.SPLIT:
                return 12 * bet.wager
            elif bet.type < BetType.STRAIGHT_UP:
                return 18 * bet.wager
            else:
                return 36 * bet.wager
        return 0

    def play_round(self, players):
        spin = self.spin()
        for player in players:
            money = 0
            for bet in player.get_bets():
                money += self.pay_out(bet, spin)
            player.wins(money)
            player.clear_bet()
        self.prev_rounds.insert(0, [spin in bet for bet in ALL_BETS])
        return np.array([spin in bet for bet in ALL_BETS])

    def get_prev_rounds(self, rounds = 2):
        prev_rounds = [self.prev_rounds[i] for i in range(rounds) if i < len(self.prev_rounds)]
        while len(prev_rounds) < rounds:
            prev_rounds.append([0 for i in range(159)])
        return prev_rounds
