import runNEATtask as runNEAT
import runHPtask as runHP
from DQNtask import dqnt
from gwgame import gw
import cPickle
import pickle
import math

with open('maps.pickle') as f:
	maps = pickle.load(f)


def id2info(id):
	if id<16:
		denom = 5
		addition=4
	else:
		denom = 3
		id-=15
		addition=7
	size = id/denom + addition
	num = id % denom
	if id % denom == 0:
		size-=1
		num = denom
	return "size"+str(size)+"-g"+str(num)

def setST(exp_id):
	if exp_id < 16 or exp_id in [18, 21, 24, 27]:
		st = g.h + g.w +10
	elif exp_id in [16, 19, 22, 25]:
		st = g.h * math.ceil(g.w/2) + math.ceil(g.w/2)
	else:
		st = 30
	return st

def saveResults(info):
	with open(info+'.pickle', 'w') as f:
 		pickle.dump((nonRandResult, randResult), f)
 	f.close()

if __name__ == "__main__":
	generation = 50
	population = 200
	test_step = 100
	epoch = generation
	step = population
	exp_id=0

	randResult = []
	nonRandResult =[]
	
	exp_id=0
	for g in maps:
		exp_id+=1
		for i in range(1):
			st = setST(exp_id)
			info = id2info(exp_id)+"_randPlayer_"+str(i+1)+"th_try"

			randPlayer=True
			HPresult = runHP.run(g, 'nhn', 'triup-down', randPlayer = randPlayer, trails = test_step, generation = generation, 
				population = population, nwin=1)
			runDQN = dqnt(g, randPlayer = randPlayer, test_num=test_step, epochs = generation, 
				steps= population, fitThreshold = 1, stepThreshold = 10)
			DQNresult = runDQN.run()
			HPresult['exp_id'] = info
			DQNresult['exp_id'] = info
			randResult.append((HPresult, DQNresult))

			saveResults(info)
		
		generation *= 1.03
		generation = int(generation)
	
	exp_id=0
	generation = 50
	for g in maps:
		exp_id+=1
		for i in range(1):
			randPlayer = False
			info = id2info(exp_id)+"_deterministic_"+str(i+1)+"th_try"
			st = setST(exp_id)

			NEATresult = runNEAT.run(g, trails = test_step, randPlayer = randPlayer, generation = generation, 
				population = population, nwin = 1)
			runDQN = dqnt(g, randPlayer = randPlayer, test_num=test_step, epochs = generation, 
				steps= population, fitThreshold = 1, stepThreshold = st)
			DQNresult = runDQN.run()
			NEATresult['exp_id'] = info
			DQNresult['exp_id'] = info

			nonRandResult.append((NEATresult, DQNresult))

			saveResults(info)



