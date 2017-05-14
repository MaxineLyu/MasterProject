from __future__ import division
### IMPORTS ###
import sys, os
from functools import partial

sys.path.append(os.path.join(os.path.split(__file__)[0],'..','..')) 
from peas.methods.neat import NEATPopulation, NEATGenotype
from peas.methods.hyperneat import HyperNEATDeveloper, Substrate
from HPtask import gwt
import numpy as np
from gwgame import gw
import drawGW as dgw


np.set_printoptions(threshold=np.nan)

def evaluate(individual, task, developer):
    stats = task.evaluate(developer.convert(individual))
    if isinstance(individual, NEATGenotype):
        stats['nodes'] = len(individual.node_genes)
    return stats
    
def solve(individual, task, developer):
    return task.solve(developer.convert(individual))

def run(game, method, setup, randPlayer=True, 
    generation=50, population=100, clock=None, nwin=None, trails = 100):
    # Create task and genotype->phenotype converter
    task = gwt(game, randPlayer=randPlayer, nwin=nwin, trails = trails)
    substrate = Substrate()
    substrate.add_nodes((game.w, game.h), 'l')
    substrate.add_connections('l', 'l')
    
    geno_kwds = dict(feedforward=True, 
                     inputs=6, 
                     weight_range=(-3.0, 3.0), 
                     prob_add_conn=0.1, 
                     prob_add_node=0.03,
                     bias_as_node=False,
                     types=['sin', 'bound', 'linear', 'gauss', 'sigmoid', 'abs'])
    
    if method == 'nhn':
        pass
    # geno_kwds['max_nodes'] = 30

    geno = lambda: NEATGenotype(**geno_kwds)
    pop = NEATPopulation(geno, popsize=population, target_species=15, max_cores=4, stop_when_solved=nwin is not None,
                         compatibility_threshold=3.0, stagnation_age=50, old_age=50, clock=clock)
	
    developer = HyperNEATDeveloper(substrate=substrate, 
                                   sandwich=True, 
                                   add_deltas=True,
                                   node_type='linear')
                               
        # Run and save results
    results = pop.epoch(generations=generation,
                        evaluator=partial(evaluate, task=task, developer=developer),
                        solution=partial(solve, task=task, developer=developer),
                        )    
    
    return results

    # Method is one of  ['wvl', 'nhn', '0hnmax', '1hnmax']
    # setup is one of ['big-little', 'triup-down']
	
