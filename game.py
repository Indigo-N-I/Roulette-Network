import random
from bets import BetType, ALL_BETS
import numpy as np
from collections import defaultdict

class Roulette():
    def __init__(self, double_zeros = True):
        self.vals = [i - int(double_zeros) for i in range(38 - int(double_zeros))]
        self.prev_rounds = []
        self.round = 0

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

    def sim_rounds(self, rounds):
        for i in range(rounds):
            spin = self.spin()
            self.prev_rounds.insert(0, [int(spin in bet) for bet in ALL_BETS])

    def play_round(self, players):
        self.round += 1
        spin = self.spin()
        stats = {
            BetType.PARITY : 0
            ,BetType.COLOR : 0
            ,BetType.HIGH_LOW : 0
            ,BetType.COLUMN : 0
            ,BetType.DOZEN : 0
            ,BetType.SNAKE : 0
            ,BetType.LINE : 0
            ,BetType.BASKET : 0
            ,BetType.CORNER : 0
            ,BetType.STREET : 0
            ,BetType.SPLIT : 0
            ,BetType.STRAIGHT_UP : 0
        }
        # print(f"the number of players is {len(players)}")
        for player in players:
            money = 0
            for bet in player.get_bets():
                stats[bet.get_type()] += 1
                money += self.pay_out(bet, spin)
            player.wins(money)
            player.clear_bet()
            # print(player.round, player.money, player)
        self.prev_rounds.insert(0, [int(spin in bet) for bet in ALL_BETS])
        if len(self.prev_rounds) > 20:
            self.prev_rounds = self.prev_rounds[:20]
        # if self.round % 1000 == 999:
        #     print(f'{self.round} rounds were played at the table')
        if self.round % 100 == 1:
            print(f"round {self.round} stats:")
            for bet in stats:
                print(bet, ":", stats[bet])
            print()
        return np.array([spin in bet for bet in ALL_BETS]).astype(int)

    def get_prev_rounds(self, rounds = 2):
        prev_rounds = [self.prev_rounds[i] for i in range(rounds) if i < len(self.prev_rounds)]
        while len(prev_rounds) < rounds:
            prev_rounds.append([0 for i in range(159)])
        return prev_rounds
