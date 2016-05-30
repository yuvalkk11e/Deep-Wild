__author__ = 'yuval'

import pygame
import sys
import animal
import plant_life
import random
import simulator
import copy

starting_population = 1
starting_bushs = 1
saved_animal = animal.animal()
map_width = 550
map_height = 550

def evaluate_animal(animal,test_limit=2000,tests_num=5):
    turns = 0
    test_limit = test_limit
    total_survived = 0
    for sim in range(tests_num):
        simulation_data = simulate_game(test_limit,[copy.deepcopy(animal)])
        turns = simulation_data[0]
        total_survived += turns
    return total_survived/tests_num

class game():
    @property
    def plants(self):
        return self.plants
    @property
    def animals(self):
        return self.animals
    @property
    def map(self):
        return self.map
    @property
    def screen_width(self):
        return self.screen_width
    @property
    def screen_height(self):
        return self.screen_height

    def most_successful(self):
        return self.most_successful

    def __init__(self,screen_width,screen_height,animals,plants):
        self.animals = animals
        self.plants = plants
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_init()
        self.most_successful = [animal.animal() for i in range(starting_population)]
        self.update_most_successful()

    def update_most_successful(self):
        if self.animals:
            self.animals = sorted(self.animals,key=lambda anim : anim.turns)
            for x in range(len(self.most_successful)):
                if x > len(self.animals)-1:
                    break
                if self.animals[x].turns > self.most_successful[x].turns:
                    self.most_successful[x] = self.animals[x]


    def map_init(self):
        self.map = []
        for x in range(self.screen_width):
            self.map.append([])
            for y in range(self.screen_height):
                self.map[x].append(1)

    def check_map(self,location):
        if location[0] < 0 or location[1] < 0 or location[0] >= self.screen_width or location[1] >= self.screen_height:
            return 0
        elif self.map[location[0]][location[1]] == 1:
            return 1
        return 0

    def random_location(self):
        return [random.random()*self.screen_width,random.random()*self.screen_height]

    def world_borders(self,location):
        if location[0]>self.screen_width:
            location[0] = 0
        if location[1]>self.screen_height:
            location[1] = 0
        if location[0]<0:
            location[0] = self.screen_width
        if location[1]<0:
            location[1] = self.screen_height
        return location

    def plant_reproduce(self,plant):
        bushes = []
        available = [[plant.location[0],plant.location[1]] for i in range(4)]
        size = int(plant.size)
        available[0][0] += size
        available[1][0] -= size
        available[2][1] += size
        available[3][1] -= size
        if self.check_map(available[0]):
            b = plant_life.bush()
            b.location = available[0]
            bushes.append(b)
        self.plants += bushes

    def brain_input(self,anim):
        '''
        input_layer = []
        input_layer.append(anim.location[0]/self.screen_width)
        input_layer.append(anim.location[1]/self.screen_height)
        d = 100000
        id = 0
        for x in range(len(self.plants)):
            if simulator.disntance(anim.location,self.plants[x].location) < d:
                d = simulator.disntance(anim.location,self.plants[x].location)
                id = x
        plant = self.plants[id]
        input_layer.append(plant.location[0]/self.screen_width)
        input_layer.append(plant.location[1]/self.screen_height)
        return input_layer
        '''
        input_layer = []
        d = 100000
        id = 0
        input_length = anim.brain.get_topology()[0]
        if self.plants:
            plants = sorted(self.plants, key = lambda plant : simulator.disntance(anim.location,plant.location))
            for plant in self.plants:
                input_layer.append(simulator.angle_between(anim.location,plant.location)/180)
                input_length -= 1
                if input_length == 0:
                    break
        for x in range(input_length):
            input_layer.append(random.randrange(-1,1,1))
        return input_layer

    def handle_plants(self):
        for plant in self.plants:
            if plant.dead():
                self.plants.remove(plant)
                break
            plant.regenerate()
            #self.plant_reproduce(plant)

    def handle_animals(self):
        #print "animals count = " + str(len(self.animals))
        children = []
        avg = 0.0
        for anim in self.animals:
            if anim.dead():
                self.animals.remove(anim)
                continue
            anim.decay()
            anim.location = self.world_borders(anim.location)
            input = self.brain_input(anim)
            output_layer = anim.brain_activity(input)
            avg += output_layer[1]
            anim.move(output_layer[0]*180)
            anim.eat(self.plants)
            if output_layer[2] > 0:
                anim.devour(self.animals)
            #child = anim.reproduce(output_layer[1]*anim.max_health.value)
            #if not child == None:
             #   children.append(child)
       # self.animals += children
        #if self.animals:
         #   print avg / len(self.animals)

    def repopulate(self,anims_bool,plants_bool):
        if anims_bool:
            for x in range(starting_population-len(self.animals)):
                anim = self.most_successful[x].copy(10)
                anim.location = self.random_location()
                self.animals.append(anim)
        if plants_bool:
            for x in range(starting_bushs-len(self.plants)):
                bush = plant_life.bush()
                bush.location = self.random_location()
                self.plants.append(bush)

def simulate_game(turns=3000,animals=animal.animal()):
    #variables
    screen_width,screen_height = map_width,map_height
    plants = [plant_life.bush() for j in range(starting_bushs)]
    for p in plants:
        p.location = simulator.convert_location([random.random()*screen_width,random.random()*screen_width])
    game_handle = game(screen_width,screen_height,animals,plants)
    for anim in animals:
        anim.health.value = anim.max_health.value
    #logic
    for turn in range(turns):
        if not game_handle.animals:
            break
        game_handle.update_most_successful()
        game_handle.handle_plants()
        game_handle.repopulate(0,1)
        game_handle.handle_animals()
    return (turn,len(game_handle.animals),game_handle.most_successful)

def run_game(screen_width=map_width,screen_height=map_height,fps=30,starting_animals=starting_population,starting_bushs=starting_bushs):

    screen_width = screen_width
    screen_height = screen_height
    screen = pygame.display.set_mode((screen_width,screen_height))

    clock = pygame.time.Clock()
    FPS = fps

    white = (255,255,255)
    black = (0,0,0)
    blue = (0,0,255)
    green = (0,255,0)
    red = (255,0,0)

    plants = [plant_life.bush() for j in range(starting_bushs)]
    if starting_animals == starting_population:
        animals = [animal.animal() for i in range(starting_animals)]
    else:
        animals = starting_animals
    for p in plants:
        p.location = simulator.convert_location([random.random()*screen_width,random.random()*screen_width])
    game_handle = game(screen_width,screen_height,animals,plants)

    pygame.init()
    #logic :
    counter = 0
    king = 0
    running = True
    while running:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                #sys.exit()
        game_handle.update_most_successful()
        for anim in game_handle.animals:
            pygame.draw.circle(screen, black, simulator.convert_location(anim.location),4,1)
        for plant in game_handle.plants:
            pygame.draw.rect(screen, green, [plant.location[0],plant.location[1],plant.size,plant.size],2)
        for x in xrange(len(game_handle.animals)):
            for y in xrange(x,len(game_handle.animals)):
                if game_handle.animals[x].brain.identical(game_handle.animals[y].brain) and not x == y:
                    print x, y
                    print "Are identical !"
        game_handle.handle_plants()
        game_handle.repopulate(1,1)
        game_handle.handle_animals()
        pygame.display.update()
        clock.tick(FPS)

