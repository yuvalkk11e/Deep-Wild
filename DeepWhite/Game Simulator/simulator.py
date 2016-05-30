__author__ = 'yuval'

import animal
import math
import random
import copy

rad = 180 / math.pi

def disntance(location1,location2):
    d1 = abs(location1[0]-location2[0])
    d2 = abs(location1[1]-location2[1])
    return d1+d2

def convert_location(location):
    return [float_int(location[0]),float_int(location[1])]

def polar_coordinates(angle,radius):
    return [math.cos(math.radians(angle))*radius,math.sin(math.radians(angle))*radius]

def angle_between(location1,location2):
    dx = location2[0] - location1[0]
    dy = location2[1] - location1[1]
    return math.atan2(dy,dx) * rad


def float_int(float):
    if float-int(float) > 0.5:
        return int(math.ceil(float))
    if float-int(float) <= 0.5:
        return int(math.floor(float))



