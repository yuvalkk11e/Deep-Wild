__author__ = 'yuval'

import random
import math
import simulator

class connection():
    @property
    def weight(self):
        return self.weight
    @property
    def delta_weight(self):
        return self.delta_weight

    @weight.setter
    def weight(self, value):
        self._weight = value
    @delta_weight.setter
    def delta_weight(self, value):
        self._delta_weight = value

    def __init__(self,weight =0.0, delta_weight=0.0):
        self.weight = weight
        self.delta_weight = delta_weight

class neuron():

    @property
    def output(self):
        return self.output

    @property
    def output_weights(self):
        return self.output_weights

    @property
    def index(self):
        return self.index

    @property
    def gradient(self):
        return self.gradient

    @property
    def eta(self):
        return self.eta

    @property
    def alpha(self):
        return self.alpha

    @output.setter
    def output(self, value):
        self._output = value

    @output_weights.setter
    def output_weights(self, value):
        self._output_weights = value

    @index.setter
    def index(self, value):
        self._index = value

    @eta.setter
    def eta(self, value):
        self._eta = value

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    @gradient.setter
    def gradient(self, value):
        self._gradient = value

    def init_weights(self,num_outputs):
        self.output_weights = []
        for x in range(num_outputs):
            value = random.randrange(-1,1,1,float)
            self.output_weights.append(connection(value))

    def __init__(self,num_outputs=1, my_index=0, gradient=0,eta=0.2,alpha=0.2):
        self.output = 0
        self.init_weights(num_outputs)
        self.index = my_index
        self.gradient = gradient
        self.eta = eta
        self.alpha = alpha


    def sum_inputs(self, prev_layer): #prev_layer of neurons
        sum = 0.0
        for n in prev_layer:
            sum += n.output * n.output_weights[self.index].weight
        sum = self.activation_function(sum)
        return sum

    def activation_function(self,number):
        value = math.tanh(number)
        return value

    def activation_function_derivative(self,number):
        value = 1.0 - number*number
        return value

    def calculate_output_gradient(self,target_value):
        delta = target_value - self.output
        self.gradient =  delta * self.activation_function_derivative(self.output)

    def sumDOW(self, next_layer):
        sum = 0.0
        for n in range(len(next_layer)-1):
            sum += self.output_weights[n].weight * next_layer[n].gradient
        return sum

    def calculate_hidden_gradient(self, next_layer):
        delta = self.sumDOW(next_layer)
        self.gradient = delta * self.activation_function_derivative(self.output)

    def update_input_weights(self, prev_layer):
        for neuron in prev_layer:
            old_delta = neuron.output_weights[self.index].delta_weight
            new_delta =  self.eta * neuron.output * self.gradient + self.alpha * old_delta
            neuron.output_weights[self.index].delta_weight = new_delta
            neuron.output_weights[self.index].weight += new_delta

    def mutate_weight(self,delta):
        rand = random.random()
        id = simulator.float_int(rand*(len(self.output_weights)-1))
        mutation_ratio = delta
        rand_value = random.randrange(-1,1,1,float) / mutation_ratio
        self.output_weights[id].weight += rand_value

    def print_weights(self):
        for w in self.output_weights:
            print "weight : " + str(w.weight)
            #print "delta_weight : " + str(w.delta_weight)

    def to_string(self):
        print "neuron state: "
        print "output : " + str(self.output)
        self.print_weights()
        print self.index
        print self.gradient

    def identical(self,neuron1):
        if not len(self.output_weights) == len(neuron1.output_weights):
            return 0
        for weight in range(len(self.output_weights)):
            if not self.output_weights[weight].weight == neuron1.output_weights[weight].weight:
                return 0
        return 1


