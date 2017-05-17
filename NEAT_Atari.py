import os
import neat
from ale_python_interface import ALEInterface
import cv2
import numpy as np
import random

ale=ALEInterface()
ale.setInt("frame_skip", 4)
ale.setInt("random_seed", 123)
#ale.setBool('sound', True)
#ale.setBool('display_screen', True)
ale.loadROM("roms/pong.bin")
acts = ale.getLegalActionSet()

def get_screen():
	screen = ale.getScreenGrayscale()
	resized = cv2.resize(screen, (1,7056))
	return resized

def gen_pop():
	config_path='config'
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
		neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	pop = neat.Population(config)
	stats=neat.StatisticsReporter()
	pop.add_reporter(stats)
	pop.add_reporter(neat.StdOutReporter(True))
	pop.add_reporter(neat.Checkpointer(25, 900))
	print "reached"
	gen_best = pop.run(e, 25)

def e(gs, config):
	actionset = ale.getLegalActionSet()
	nets=[]
	for gid, g in gs:
		nets.append((g, neat.nn.FeedForwardNetwork.create(g, config)))
	for g, net in nets:
		ale.reset_game()
		r=0.0
		while not ale.game_over():
			o=get_screen()
			if random.random()<0.2:
				action = actionset[np.random.randint(actionset.size)]
			else:
				output = net.activate(o)
				action = np.argmax(output)
			r+=ale.act(action)
		print(r)
		g.fitness = r

if __name__ == '__main__':
	gen_pop()