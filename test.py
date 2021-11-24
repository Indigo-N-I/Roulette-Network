from player import ColorBetter
from game import Roulette
import numpy as np
import matplotlib.pyplot as plt
from network_player import NetworkPlayer
from network import NerualNetwork, cross_networks, ReluLayer, FlattenLayer, OutputLayer
import random
from fitness import PlayerData
import time

table1 = Roulette()

def test(test_players, rounds = 5000):

    for i in range(rounds):
        for test_player in test_players:
            # print(test_player.network)
            if not test_player.can_play():
                test_player.reset()
            test_player.make_bets(table1.get_prev_rounds(5))

        # if i % 100 == 99:
        #     print(f'done with {i} rounds')

        table1.play_round(test_players)

def make_neural_player():
    layer1 = 64
    layer2 = 32
    flatten = FlattenLayer(159, np.array([random.random() - .5 for i in range(159)]), 159)
    # print(flatten.weights)
    relu = ReluLayer(5, np.array([[random.random() - .5 for i in range(5)] for i in range (layer1)]), layer1)
    # print(relu.weights)
    relu1 = ReluLayer(layer1, np.array([[random.random() - .5 for i in range(layer1)] for i in range (layer2)]), layer2)
    output = OutputLayer(layer2, np.array([[random.random() - .5 for i in range(layer2)] for i in range (160)]), 160)
    # print(output.weights)

    network = NerualNetwork()
    network.add_layer(flatten)
    network.add_layer(relu)
    network.add_layer(relu1)
    network.add_layer(output)

    return NetworkPlayer(network = network, start_money = 5000)

def get_one(possible, fitness, out_of = 3):
    a = [random.choice(possible) for i in range(3)]
    # print([fitness(c) for c in a])
    b = max(a, key = fitness)
    # print(fitness(b))
    return b

def get_mating_pairs(possible, fitness, num_pairs, outof = 3):
    # print(possible)
    return [(get_one(possible, fitness, outof), get_one(possible, fitness, outof)) for i in range(num_pairs)]

def fitness(participant):
    return participant.avg_rounds() - (participant.avg_num_bets() - 5) ** 1.1

TOTAL_PLAYERS = 100
GENERATIONS = 200
rounds = 2000
players = []
best_fitness = 0
for i in range(TOTAL_PLAYERS):
    players.append(make_neural_player())

table1.sim_rounds(5)

for i in range(GENERATIONS):
    test(players, int(rounds))
    players.sort(key = lambda x: fitness(x), reverse = True)
    fit = players[0].avg_rounds()
    rounds = players[0].avg_rounds() * 25
    print(f'At generation {i + 1} the fitness was {fit}, best fit player has played {players[0].total_games()}')
    print([fitness(player) for player in players])
    if fit > best_fitness:
        best_fitness = fit
        players[0].save(f'round{i}_fitness{fit}.txt')
    players = players[:TOTAL_PLAYERS]
    # print([fitness(player) for player in players])
    mating_pairs = get_mating_pairs(players, fitness, TOTAL_PLAYERS//2, 5)

    for pair in mating_pairs:
        players.append(pair[0].mate(pair[1]))
