__author__ = 'yuval'

import Network
import random
import math
import simulator
from copy import deepcopy


class attribute():
    @property
    def name(self):
        return self.name
    @property
    def value(self):
        return self.value
    @property
    def max_value(self):
        return self.max_value

    def __init__(self,value=1.0,max_value=1.0,name="speed"):
        self.value = value
        self.max_value = max_value
        self.name = name

attributes = 9

class animal():

    @property
    def speed(self):
        return self.speed

    @property
    def health(self):
        return self.health

    @property
    def max_health(self):
        return self.max_health

    @property
    def dmg(self):
        return self.dmg

    @property
    def speed(self):
        return self.speed

    @property
    def armor(self):
        return self.armor

    @property
    def size(self):
        return self.brain

    @property
    def brain(self):
        return self.brain

    @property
    def name(self):
        return self.name

    @property
    def location(self):
        return self.location

    @property
    def turns(self):
        return self.turns

    def __init__(self,speed=None,health=None,max_health=None,dmg=None,armor=None,size=None,brain=None,name="Yuval",location=None,turns=0):
        if speed == None:
            speed = attribute()
        if health == None:
            health = attribute()
        if max_health == None:
            max_health = attribute()
        if dmg == None:
            dmg = attribute()
        if armor == None:
            armor = attribute()
        if size == None:
            size = attribute()
        if location == None:
            location = [400,400]
        self.location = location
        if brain == None:
            brain = [3,2,3]
        brain1 = Network.network(brain)
        self.brain = brain1
        self.speed = speed
        self.health = health
        self.max_health = max_health
        self.dmg = dmg
        self.armor = armor
        self.size = size
        self.name = name
        self.speed.value = 20
        self.turns = turns

    def turn_tick(self):
        self.turns += 1

    def reproduce(self,transfer,delta=10,layer_num=None,neuron_num=None):
        if self.health.value >= transfer and transfer > 0.0:
            self.health.value -= transfer
            offspring = deepcopy(self)
            offspring.health.value = transfer
            offspring.mutate(delta)
            return offspring

    def copy(self,delta=10,layer_num=None,neuron_num=None):
        offspring = deepcopy(self)
        offspring.health.value = offspring.max_health.value
        offspring.mutate(delta,layer_num,neuron_num)
        return offspring

    def identical(self, animal1):
        return self.brain.identical(animal1.brain)

    def brain_mutate(self,delta=10,layer_num=None,neuron_num=None):
        self.brain.mutate_neuron(delta,layer_num,neuron_num)

    def mutate(self,delta=10,layer_num=None,neuron_num=None):
        self.brain_mutate(delta,layer_num,neuron_num)

    def heal(self):
        self.health.value = self.max_health.value

    def move(self,angle):
        polar_move = simulator.polar_coordinates(angle,self.speed.value)
        self.location[0] += polar_move[0]
        self.location[1] += polar_move[1]

    def eat(self,plants):
        for bush in plants:
            loc = simulator.convert_location(self.location)
            if simulator.disntance(loc,bush.location) <= self.size.value * 10:
                self.health.value += bush.value
                bush.value = 0.0
            #if self.health.value > self.max_health.value:
             #   self.health.value = self.max_health.value

    def devour(self,animals):
        for anim in animals:
            if anim == self:
                continue
            if simulator.disntance(self.location,anim.location) <= self.size.value * 10:
                if self.dmg.value > anim.health.value:
                    self.health.value += anim.health.value
                else:
                    self.health.value += self.dmg.value
                anim.health.value -= self.dmg.value
            #if self.health.value > self.max_health.value:
             #   self.health.value = self.max_health.value

    def decay(self):
        self.health.value -= 0.02
        self.turn_tick()

    def dead(self):
        if self.health.value <= 0.0:
            return 1
        return 0

    def brain_input(self):
        input_layer = self.brain.get_topology()[0]
        input_values = []
        for x in range(input_layer):
            input_values.append(random.random())
        return input_values

    def brain_output(self):
        output_layer = self.brain.get_results()
        return output_layer

    def brain_activity(self,input_values,target_values=None):
        #input_values = self.brain_input()
        self.brain.handle_activity(input_values,target_values)
        return self.brain_output()

    def to_string(self):
        print "health = " + str(self.health.value)

        #self.brain.to_string()



