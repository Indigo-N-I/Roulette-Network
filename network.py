from bets import ALL_BETS
from player import Player
import random
from abc import ABC, abstractmethod
import numpy as np
import copy
from scipy.special import softmax

# network will take in a LOOK_BACK x 160 input
# each layer will be 1's and 0's for wich bets won with the first index being if the user won said round
# will come out with a 1 x 160 output
# index 0: how much to bet, percentage of remaining money
# successive index: how much of the bet is getting put on each bet index

class NetworkLayer(ABC):
    def __init__(self, input_shape, weights, output_shape):
        self.input_shape = input_shape
        self.weights = weights
        self.output_shape = output_shape
        super().__init__()

    @abstractmethod
    def forward(self, input):
        pass

    def get_weights(self):
        return self.weights

    def set_weights(self, weights):
        self.weights = weights

class ReluLayer(NetworkLayer):
    def __init__(self, input_shape, weights, output_shape, relu_constant = 1):
        self.relu_constant = 1
        assert weights.shape == (output_shape, input_shape), f'{weights.shape} != {(input_shape, output_shape)}'
        super().__init__(input_shape, weights, output_shape)

    def forward(self, input):
        def relu(value):
            return value * self.relu_constant * (value > 0)

        # print(input)

        output = np.sum(input * self.weights, axis = 1)
        assert output.shape[0] == self.output_shape, f'output.shape {output.shape} != output_shape {self.output_shape}'
        return relu(output)

class FlattenLayer(NetworkLayer):
    def __init__(self, input_shape, weights, output_shape):
        super().__init__(input_shape, weights, output_shape)

    def forward(self, input):
        def relu(value):
            return value  * (value > 0)

        # print(input)
        # print("weights", self.weights)
        pre_flip = np.matmul(input, self.weights)
        # print(pre_flip)
        return relu(pre_flip).T

class OutputLayer(ReluLayer):
    def __init__(self, input_shape, weights, output_shape, relu_constant = 1):
        super().__init__(input_shape, weights, output_shape, relu_constant = 1)

    def forward(self, input):
        def relu(value):
            return value * self.relu_constant * (value > 0)

        def sigmoid(x):
            return 1/(1 + np.exp(-x))

        # print(input)
        output = relu(np.sum(input * self.weights, axis = 1))

        # print(output)
        output[0] = sigmoid(output[0])
        output[1:] = softmax(output[1:])
        # print(output)

        return output


class NerualNetwork():
    def __init__(self):

        self.network_stack = []

    def add_layer(self, layer):
        self.network_stack.append(layer)

    def forward(self, input):
        x = input
        for layer in self.network_stack:
            x = layer.forward(x)
            # print(x)
        return x

    def get_weights(self):
        return [layer.get_weights() for layer in self.network_stack]

    def get_layers(self):
        return self.network_stack

def drift(array, prob = .3, dist = .2):
    changing = np.random.random(array.shape)
    drift_amt = np.random.random(array.shape) * dist - (dist/2)

    changing = changing < prob
    array += changing * drift_amt
    return array

def cross_networks(nn1, nn2):
    nn1_weights = nn1.get_weights()
    nn2_weights = nn2.get_weights()
    network_layers = nn1.get_layers()

    new_network = NerualNetwork()
    assert len(nn1_weights) == len(nn2_weights), f"not the same number of layers for the two networsk {len(nn1_weights)} vs {len(nn2_weights)}"
    for i in range(len(nn1_weights)):
        from_nn1 = np.random.randint(2, size = nn1_weights[i].shape)
        assert len(nn1_weights[i]) == len(nn2_weights[i]), f'layer does not have same number of weights {len(nn1_weights)[i]} vs {len(nn2_weights)[i]}'
        weight_layer = nn1_weights[i] * from_nn1 + nn2_weights[i] * (np.abs(from_nn1 - 1))
        weight_layer = drift(weight_layer)
        new_layer = network_layers[i]
        # print(type(new_layer))
        new_layer.set_weights(weights = weight_layer)
        new_network.add_layer(new_layer)

    return new_network

if __name__ == '__main__':
    LOOK_BACK = 5
    test_input = np.array([[random.random() for i in range(160)] for i in range(LOOK_BACK)])

    test_network = NerualNetwork()
    test_network1 = NerualNetwork()

    flatten = FlattenLayer(160, np.array([random.random() for i in range(160)]), 160)
    flatten1 = FlattenLayer(160, np.array([random.random() for i in range(160)]), 160)
    relu = ReluLayer(5, np.array([[random.random() for i in range(5)] for i in range (12)]), 12)
    output = OutputLayer(12, np.array([[random.random() for i in range(12)] for i in range (12)]), 12)
    relu1 = ReluLayer(5, np.array([[random.random() for i in range(5)] for i in range (12)]), 12)

    x = flatten.forward(test_input)
    # print(relu.forward(x))

    test_network.add_layer(flatten)
    test_network.add_layer(relu)
    test_network.add_layer(output)
    test_network1.add_layer(flatten1)
    test_network1.add_layer(relu1)

    print(test_network.forward(test_input))
    # print(cross_networks(test_network, test_network1).forward(test_input))
