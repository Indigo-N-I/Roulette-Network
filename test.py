from player import ColorBetter
from game import Roulette
import numpy as np
import matplotlib.pyplot as plt
from network_player import NetworkPlayer
from network import NerualNetwork, cross_networks, ReluLayer, FlattenLayer, OutputLayer
import random
from fitness import PlayerData

def test(test_player, TEST = 1000):
    table1 = Roulette()
    rounds = []
    max_money = []

    for i in range(TEST):
        test_player.reset()
        round = 0
        if i % 100 == 99:
            print(f'done with {i} tests')

        player_money = test_player.money
        prev_round = 0

        while test_player.can_play() and prev_round != player_money:
            player_money = test_player.money
            test_player.make_bets(table1.get_prev_rounds(5))
            table1.play_round([test_player])
            # if round %1000 == 0:
            #     print(f"test_player has {test_player.money} dollars")
            prev_round = test_player.money
            round += 1

        max_money.append(test_player.get_max_money())
        rounds.append(round)

    return PlayerData(test_player, max_money, rounds)

def make_neural_player():
    flatten = FlattenLayer(159, np.array([random.random() - 1 for i in range(159)]), 159)
    relu = ReluLayer(5, np.array([[random.random() - 1 for i in range(5)] for i in range (64)]), 64)
    output = OutputLayer(64, np.array([[random.random() - 1 for i in range(64)] for i in range (160)]), 160)

    network = NerualNetwork()
    network.add_layer(flatten)
    network.add_layer(relu)
    network.add_layer(output)

    test_player = NetworkPlayer(network = network, start_money = 5000)
    return test_player

def get_mating_pairs(possible):
    return [(random.randint(0,possible -1), random.randint(0,possible -1)) for i in range(possible)]

TOTAL_PLAYERS = 20
GENERATIONS = 200
GAMES = 50
players = []
for i in range(TOTAL_PLAYERS):
    players.append(test(make_neural_player(), GAMES))

for i in range(GENERATIONS):
    players.sort(key = lambda x: x.median_money())
    print(f'At generation {i + 1} the median genearted was {players[-1].median_money()}')
    players = players[TOTAL_PLAYERS//2:]
    mating_pairs = get_mating_pairs(TOTAL_PLAYERS//2)

    for pair in mating_pairs:
        players.append( test(players[pair[0]].get_player().mate(players[pair[1]].get_player()), GAMES))
