from peas.methods.neat import NEATPopulation, NEATGenotype
from NEATtask import gwt
from gwgame import gw
import pygraphviz as pgv

def run(g, trails = 100, population = 100, generation = 100, nwin=1, randPlayer = False):
    genotype = lambda: NEATGenotype(inputs=g.w * g.h, outputs=4,
                                    weight_range=(-50., 50.), 
                                    types=['linear'])
    
    pop = NEATPopulation(genotype, target_species=15, popsize=population, 
    	stop_when_solved=nwin is not None)
    
    t = gwt(g, randPlayer = randPlayer, trails = trails, nwin = nwin)
    results = pop.epoch(generations = generation, evaluator = t.evaluate, 
    	solution = t.solve)
    # net=results['champions'][-1]
    # net.visualize("NEATchamp.png")
    # G=pgv.AGraph("NEATchamp.dot")
    # G.draw('NEATchamp.png', format='png', prog='dot')
    return results