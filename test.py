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

def test(test_player, TEST = 1000):
    rounds = []
    max_money = []

    for i in range(TEST):
        test_player.reset()
        round = 0
        if i % 100 == 99:
            print(f'done with {i} tests')

        player_money = test_player.money
        prev_round = 0

        # tic1 = time.perf_counter()
        # round_time = []
        while 1:
            # tic = time.perf_counter()
            if not (test_player.can_play() and prev_round != player_money):
                break
            player_money = test_player.money
            test_player.make_bets(table1.get_prev_rounds(5))
            table1.play_round([test_player])

            # if round %1000 == 0:
            #     print(f"test_player has {test_player.money} dollars")
            prev_round = test_player.money
            round += 1
            # toc = time.perf_counter()
            # round_time.append(toc - tic)
        # toc1 = time.perf_counter()
        # print(f"Round done in the tutorial in {toc1 - tic1:0.4f} with avg of {np.mean(round_time)} seconds\
              # , over {round} rounds")
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

    return NetworkPlayer(network = network, start_money = 5000)

def get_one(possible, fitness, out_of = 3):
    return max([random.choice(possible) for i in range(3)], key = fitness)

def get_mating_pairs(possible, fitness, num_pairs):
    # print(possible)
    return [(get_one(possible, fitness), get_one(possible, fitness)) for i in range(num_pairs)]

def fitness(participant):
    return participant.median_rounds()

TOTAL_PLAYERS = 50
GENERATIONS = 200
GAMES = 20
players = []
best_fitness = 0
for i in range(TOTAL_PLAYERS):
    players.append(test(make_neural_player(), GAMES))

for i in range(GENERATIONS):
    players.sort(key = lambda x: fitness(x), reverse = True)
    fit = fitness(players[0])
    print(f'At generation {i + 1} the fitness was {fit}')
    print([fitness(player) for player in players])
    if fit > best_fitness:
        best_fitness = fit
        players[0].save(f'round{i}_fitness{fit}.txt')
    players = players[:TOTAL_PLAYERS]
    mating_pairs = get_mating_pairs(players, fitness, TOTAL_PLAYERS//2)

    for pair in mating_pairs:
        players.append( test(pair[0].get_player().mate(pair[1].get_player()), GAMES))
