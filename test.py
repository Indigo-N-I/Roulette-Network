from player import ColorBetter
from game import Roulette
import numpy as np
import matplotlib.pyplot as plt

table1 = Roulette()
rounds = []
max_money = []

TEST = 10000

for i in range(TEST):
    test_player = ColorBetter(5000)
    round = 0
    if i % 1000 == 999:
        print(f'done with {i} tests')

    while test_player.can_play():
        round += 1
        test_player.make_bets()
        table1.play_round([test_player])

    max_money.append(test_player.get_max_money())
    rounds.append(round)

print('finished tests')
# print(rounds)
# max_money = np.array(max_money)
# rounds = np.array(rounds)
print(f"Rounds: \n  {np.max(rounds)} max\n  {np.min(rounds)} min \n  {np.mean(rounds)} avg\n  {np.median(rounds)} median\n  {np.std(rounds)} std")
print(f'Max Money:\n  {np.max(max_money)} max \n  {np.min(max_money)} min \n  {np.mean(max_money)} avg\n  {np.median(max_money)} median\n  {np.std(rounds)} std')
