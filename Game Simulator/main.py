__author__ = 'yuval'

import animal
import pygame
import simulator
import Network
import random
import game
import copy

testing = "simulation2"

def draw_statistics(screen,arr_values):
    if arr_values and len(arr_values)%2 == 0 :
        screen.fill((255,255,255))
        pygame.draw.lines(screen,(0,0,255),False,arr_values,1)
        pygame.display.update()
        return True
    return False

if testing == "Network":
    topology = [2,1]
    input_values1 = [0.25,1]#[1,0.8,0.6,0.4,0.2,0.0]
    input_values2 = [1,0.5]
    target_values1 = [1]
    target_values2 = [0]
    a = Network.network(topology)
    a.to_string()
    b = Network.network(topology)
    if a.identical(b):
        print "WOW"
    for rep in range(100):
        if random.random() >= 0.5:
            input_values = input_values1
        else :
            input_values = input_values2
        a.feed_forward(input_values)
        if input_values == [0.25,1]:
            a.backProp(target_values1)
        else:
            a.backProp(target_values2)
        print rep
        print input_values
        print a.get_results()
    a.to_string()

elif testing == "animal":
    anim1 = animal.animal()
    anim2 = anim1.reproduce()
    anim1.brain_output()
#    anim1.mutate()
 #   anim1.to_string()
  #  anim2.to_string()

elif testing == "game":
    game.run_game()

elif testing == "simulator":
    p1 = [0,0]
    p2 = [0,90]
    simulator.angle_between(p1,p2)
    print simulator.polar_coordinates(90,1)

elif testing == "simulation1":
    turns = 0
    attempts = 10000
    best_animals = []
    for sim in range(attempts):
        animals = [animal.animal() for i in range(1)]
        animals[0].health.value = 2.0
        simulation_data = game.simulate_game(3000,animals)
        turns = simulation_data[0]
        animals = simulation_data[1]
        anim = simulation_data[2][0]
        print turns,animals
        if turns > 2500:
            best_animals.append(anim)
            break
    if best_animals:
        for sim in range(10):
            best_animals[0].health.value = best_animals[0].max_health.value + 1.0
            print best_animals
            simulation_data = game.simulate_game(3000,copy.deepcopy(best_animals))
            turns = simulation_data[0]
            animals = simulation_data[1]
            print turns,animals
        game.run_game(800,800,30,best_animals)

elif testing == "simulation2":
    turns = 0
    attempts = 1500
    population = 1
    best_animals = [animal.animal() for i in range(population)]
    test_limit = 2000
    delta_turn = 40.0/(test_limit-50)
    test_subjects = []
    test_counts = 5
    record = 300

    topology = best_animals[0].brain.get_topology()
    testing_layer = 0
    testing_neuron = 1
    testing_quality = 1
    found = False
    generations_scorelist = [(0,0)]
    pygame.init()
    screen_width = game.map_width
    screen_height = game.map_height
    screen = pygame.display.set_mode((screen_width,screen_height))
    for sim in range(attempts):
        for event in pygame.event:
            if event in
        turns = game.evaluate_animal(best_animals[0])
        gen_score = screen.get_height() - screen.get_height()*(turns/test_limit)
        generations_scorelist.append((sim,gen_score))
        draw_statistics(screen,generations_scorelist)
        delta = delta_turn*turns
        print delta
        print "current organism : " + str(turns)
        test_subjects = [best_animals[0].copy(delta,testing_layer,testing_neuron) for i in range(test_counts)]
        for subj in test_subjects:
            sub_turns = game.evaluate_animal(subj)
            print sub_turns
            if sub_turns > turns:
                best_animals = [subj]
                print "switched"
                if turns > record+200:
                    record = turns
                    game.run_game(800,800,30,copy.deepcopy(best_animals))
                found = True
                testing_quality += 1
                break
        if found:
            found = False
            continue
        #mutate slightly for new descending location
        if testing_quality == 0:
            testing_neuron += 1
            if testing_neuron == topology[testing_layer]:
                testing_neuron = 0
                testing_layer += 1
            if testing_layer == len(topology)-1:
                testing_layer = 0
            print "Changed Neuron"
            print testing_layer, testing_neuron
        else:
            testing_quality -= 1
            for anim in best_animals:
                anim.mutate(delta*2)

elif testing == "general":
    arr_values = []
    for x in xrange(game.map_width):
        arr_values.append(random.random()*game.map_height)
    draw_statistics(arr_values)
