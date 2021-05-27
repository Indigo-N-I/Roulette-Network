from network import NerualNetwork, cross_networks, ReluLayer, FlattenLayer
from player import Player
from bets import ALL_BETS, ALL_BETS_ENUM, Bet
import numpy as np


# temporarly not letting players know if they won previous rounds
class NetworkPlayer(Player):
    def __init__(self, network, start_money = 1000):
        self.network = network
        super().__init__(start_money)

    def make_bets(self, prev_rounds):
        pre_process = self.network.forward(prev_rounds)
        max_amount = np.max([self.money * pre_process[0], 200])
        # if max_amount > self.money:
        #     max_amount = self.money

        individual_bets = np.floor(max_amount * pre_process[1:])
        total_bets = np.sum(individual_bets)
        self.money -= total_bets

        self.bets = [Bet(individual_bets[i], ALL_BETS_ENUM[i], ALL_BETS[i]) for i in range(len(individual_bets))\
                     if individual_bets[i] != 0]

        self.won = 0

    def wins(self, money):
        self.money += money
        if self.money > self.max_money:
            self.max_money = self.money

        self.won = 1

    def won(self):
        return self.won

    def get_network(self):
        return self.network

    def mate(player1, player2):
        nn1 = player1.get_network()
        nn2 = player2.get_network()
        new_network = cross_networks(nn1, nn2)
        new_player = NetworkPlayer(network = new_network, start_money = player1.start_money)
        return new_player


if __name__ == 'main':
    test_network = NerualNetwork()
    test_network1 = NerualNetwork()

    flatten = FlattenLayer(160, np.array([random.random() for i in range(160)]), 160)
    flatten1 = FlattenLayer(160, np.array([random.random() for i in range(160)]), 160)
    relu = ReluLayer(5, np.array([[random.random() for i in range(5)] for i in range (12)]), 12)
    relu1 = ReluLayer(5, np.array([[random.random() for i in range(5)] for i in range (12)]), 12)

    x = flatten.forward(test_input)
    # print(relu.forward(x))

    test_network.add_layer(flatten)
    test_network.add_layer(relu)
    network_player = NetworkPlayer(network = test_network)
    test_input = np.array([[0 for i in range(160)] for i in range(5)])

    network_player.make_bets()
