from game import Roulette
import numpy as np
import random
from handmade_network import Network

table1 = Roulette()
fitness_info = []
INPUTS = 5
def make_neural_player():
    return Network(INPUTS)

def fitness(player):
    return player.get_rounds()

def test(test_players, rounds = 5000):

    for i in range(rounds):
        for test_player in test_players:
            # print(test_player.network)
            if not test_player.can_play():
                fitness_info.append(test_player.get_id, fitness(test_player))
            test_player.make_bets(table1.get_prev_rounds(INPUTS))

        # if i % 100 == 99:
        #     print(f'done with {i} rounds')

        table1.play_round(test_players)

TOTAL_PLAYERS = 5
GENERATIONS = 200
rounds = 2000
players = []
best_fitness = 0
for i in range(TOTAL_PLAYERS):
    players.append(make_neural_player())

test(players)