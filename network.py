from bets import ALL_BETS
from player import Player
import random
from abc import ABC, abstractmethod
import numpy as np

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

        output = np.sum(input * self.weights, axis = 1)
        assert output.shape[0] == self.output_shape, f'output.shape {output.shape} != output_shape {self.output_shape}'
        return relu(output)

class FlattenLayer(NetworkLayer):
    def __init__(self, input_shape, weights, output_shape):
        super().__init__(input_shape, weights, output_shape)

    def forward(self, input):
        def relu(value):
            return value  * (value > 0)

        pre_flip = np.matmul(input, self.weights)
        return relu(pre_flip).T

class NerualNetwork():
    def __init__(self):

        self.network_stack = []

    def add_layer(self, layer):
        self.network_stack.append(layer)

    def forward(self, input):
        x = input
        for layer in self.network_stack:
            x = layer.forward(x)
        return x

    def get_weights(self):
        return [layer.get_weights() for layer in self.network_stack]


if __name__ == '__main__':
    LOOK_BACK = 5
    test_input = np.array([[random.random() for i in range(160)] for i in range(LOOK_BACK)])

    test_network = NerualNetwork()
    flatten = FlattenLayer(160, np.array([random.random() for i in range(160)]), 160)
    relu = ReluLayer(5, np.array([[random.random() for i in range(5)] for i in range (12)]), 12)

    x = flatten.forward(test_input)
    print(relu.forward(x))

    test_network.add_layer(flatten)
    test_network.add_layer(relu)
    print(test_network.forward(test_input))
