__author__ = 'yuval'

import Neuron
import math
import random
import simulator

class network():

    @property
    def layers(self):
        return self.layers

    @layers.setter
    def layers(self,value):
        self.layers = value

    @property
    def size(self):
        return self.size

    @size.setter
    def size(self, value):
        self.size = value

    @property
    def error(self):
        return self.error

    @error.setter
    def error(self, value):
        self._error = value

    def __init__(self, topology):
        self.layers = []
        #build Neural Network architecture
        for layer in range(len(topology)):
            self.layers.append([])
            if layer == len(topology)-1:
                for neuron in range(topology[layer]):
                    self.layers[layer].append(Neuron.neuron(0,neuron))
            else:
                for neuron in range(topology[layer]+1):
                    self.layers[layer].append(Neuron.neuron(topology[layer+1],neuron))
                    if neuron == topology[layer]:
                        self.layers[layer][neuron].output = 1

        self.size = len(self.layers)
        self.error = 0.0

    def get_topology(self):
        topology = []
        for layer in self.layers:
            topology.append(len(layer))
        return topology

    def feed_forward(self, input_values):
        #init first layer:
        for x in range(len(self.layers[0])-1): ##the -1 is for not changing BIAS NEURON
            self.layers[0][x].output = input_values[x]
        #prop forward
        for x in range(1,len(self.layers)):
            if x == len(self.layers) -1:
                for neuron in range(len(self.layers[x])):
                    self.layers[x][neuron].output = self.layers[x][neuron].sum_inputs(self.layers[x-1])
            else:
                for neuron in range(len(self.layers[x])-1): #The -1 is for not setting BIAS NEURON's output
                    self.layers[x][neuron].output = self.layers[x][neuron].sum_inputs(self.layers[x-1])

    def backProp(self, target_values):
        error = 0.0
        out_layer = self.layers[self.size-1]
        for n in range(len(out_layer)):
            error += math.pow(target_values[n] - out_layer[n].output,2)
        error /= len(out_layer)
        error = math.sqrt(error)
        self.error = error
        for n in range(len(out_layer)):
            out_layer[n].calculate_output_gradient(target_values[n])

        for x in range(len(self.layers)-2,0,-1):  #iterate through all hidden layers
            hidden_layer = self.layers[x]
            next_layer = self.layers[x+1]
            for n in range(len(hidden_layer)):
                hidden_layer[n].calculate_hidden_gradient(next_layer)

        for x in range(len(self.layers)-1,0,-1):
            layer = self.layers[x]
            previous_layer = self.layers[x-1]
            for n in layer:
                n.update_input_weights(previous_layer)

    def handle_activity(self,input_values,target_values=None):
        self.feed_forward(input_values)
        if not target_values == None:
            self.backProp(target_values)
        self.get_results()

    def mutate_neuron(self,delta,layer_num=None,neuron_num=None):
        if layer_num == None:
            rand = random.random()
            layer_num = simulator.float_int(rand*(len(self.layers)-2))
        if neuron_num == None:
            rand = random.random()
            neuron_num = simulator.float_int(rand*(len(self.layers[layer_num])-1))
        self.layers[layer_num][neuron_num].mutate_weight(delta)

    def get_results(self):
        result_vals = []
        for n in self.layers[self.size-1]:
            result_vals.append(n.output)
        return result_vals

    def to_string(self):
        for layer in self.layers:
            for neuron in layer:
                neuron.to_string()

    def identical(self,network1):
        if not len(self.layers) == len(network1.layers):
            return 0
        for layer in range(len(self.layers)):
            current_layer = self.layers[layer]
            op_layer = network1.layers[layer]
            if not len(current_layer) == len(op_layer):
                return 0
            for neuron in range(len(self.layers[layer])):
                op_neuron = op_layer[neuron]
                if not current_layer[neuron].identical(op_neuron):
                    return 0
        return 1



