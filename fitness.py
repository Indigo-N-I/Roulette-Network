import numpy as np

class PlayerData():
    def __init__(self, player, max_money, rounds):
        self.player = player
        # print(max_money)
        self.max_money = max_money
        self.rounds = rounds

    def max_max_money(self):
        return np.max(self.max_money)

    def max_rounds(self):
        return np.max(self.rounds)

    def most_spent(self):
        return player.amount_bet()

    def median_money(self):
        return np.median(self.max_money)

    def median_rounds(self):
        return np.median(self.rounds)

    def get_player(self):
        return self.player

    def __str__(self):
        return f'Rounds: \n  {np.max(self.rounds)} max\n  {np.min(self.rounds)} min \n  {np.mean(self.rounds)} avg\n  {np.median(self.rounds)} median\n  {np.std(self.rounds)} std\
                \nMax Money:\n  {np.max(self.max_money)} max \n  {np.min(self.max_money)} min \n  {np.mean(self.max_money)} avg\n  {np.median(self.max_money)} median\n  {np.std(self.rounds)} std'
