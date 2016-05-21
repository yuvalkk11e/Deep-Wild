__author__ = 'yuval'

import random
import math


class bush():
    @property
    def size(self):
        return self.size
    @property
    def value(self):
        return self.value
    @property
    def max_value(self):
        return self.max_value
    @property
    def regeneration(self):
        return self.regeneration
    @property
    def division_rate(self):
        return self.division_rate
    @property
    def location(self):
        return self.location
    @location.setter
    def location(self, value):
        self._location = value

    def __init__(self,size=5.0,value=1.0,max_value=1.0,regeneration=0.5,division_rate=1.0,location=None):
        if location == None:
            location = [1,1]
        self.location = location
        self.size = size
        self.value = value
        self.max_value = max_value
        self.regeneration = regeneration
        self.division_rate = division_rate

    def regenerate(self):
        if self.value < self.max_value:
            self.value += self.regeneration

    def dead(self):
        if self.value <= 0.0:
            return True
        return False

    def to_string(self):
        print self.location


