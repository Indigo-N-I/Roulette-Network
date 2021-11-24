import numpy as np
import random

def gen_id():
    return random.randint(0, 0x10000000)

def decode_id(id):
    # convert to binary string
    num = bin(id)[2:]
    source_type = int(num[0],2)
    source_id = int(num[1:8], 2)
    dest_type = int(num[8], 2)
    dest_id = int(num[9:16], 2)
    weight = int(num[16:], 2)
    return source_type, source_id, dest_type, dest_id, weight

def sigmoid(num):
    return 1/(1+ np.exp(-num))

class Network():

    # network will take some number of inputs (previous rounds + total amount of money left)
    # the network will then use the identifier to signal where the connections are and how strong the connections are
    # identifiers will be hexadecimal code
    #  1 - Source type
    #  7 - Source ID
    #  1 - Dest type
    #  7 - Dest ID
    #  16 - weight

    def __init__(self, inputs, identifier = None, internal_nodes = 1):
        if not identifier:
            # if there is no identifier, then make identifier
            # default will be 16
            # there are 160 outputs
            self.id = [gen_id() for i in range(16)]
            self.info = [decode_id(id) for id in self.id]
        else:
            self.id = identifier
            self.info = [decode_id(id) for id in self.id]

        # connections will be created as a matrix so that we can use matrix multiplication for weights
        # network will be nx1 inputs, mx1 internal and 160x1 output
        # will have four distinct matrixes for connections
        # input-> output, input-> internal, internal-> output, internal-> internal
        self.inputs = inputs
        self.internal_nodes = internal_nodes
        self.internal_nodes_val = np.zeros(shape = (internal_nodes, 1))
        self.in_to_out = np.zeros(shape = (inputs, 160))
        self.in_to_int = np.zeros(shape = (inputs,internal_nodes))
        self.int_to_int = np.zeros(shape = (internal_nodes, internal_nodes))
        self.int_to_out = np.zeros(shape = (internal_nodes, 160))

        self.input_weights()

    def input_weights(self):
        # puts the designated weights into the arrays
        for source, s_id, dest, d_id, weight in self.info:
            weight = weight / 0b10000000000000
            if source == 0 and dest == 1: # if it starts from input and goes to output
                self.in_to_out[s_id % self.inputs][d_id %160] = weight
            elif source == 0 and dest == 0:
                self.in_to_int[s_id % self.inputs][d_id % self.internal_nodes] = weight
            elif source == 1 and dest == 0:
                self.int_to_int[s_id % self.internal_nodes][d_id % self.internal_nodes] = weight
            elif source == 1 and dest == 1:
                self.int_to_out[s_id % self.internal_nodes][d_id % 160] = weight

    def step(self, inputs):
        # go from inputs to internal nodes
            # then sigmoid
        # then go from inputs to output nodes
        # then go internal to internal
            # then sigmoid
        # finally internal to output
            # then sigmoid
            # and softmax last 159

        self.internal_nodes_val = sigmoid(np.matmul(inputs, self.in_to_int).T)
        self.output_vals = np.matmul(inputs, self.in_to_out).T
        self.internal_nodes_val = sigmoid(np.matmul(self.internal_nodes_val, self.int_to_int).T)
        self.output_vals += np.matmul(self.internal_nodes_val, self.int_to_out).T
        self.output_vals = sigmoid(self.output_vals)

        # because output values need to go from 0 -> 1
        self.output_vals += 1
        self.output_vals /= 2

        return self.output_vals[0], self.output_vals[1:]
