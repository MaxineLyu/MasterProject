from runHPTask import *
from gwgame import gw
import numpy as np
np.set_printoptions(threshold=np.nan)

g=gw()
developer, task, results=run(g, 'nhn', 'triup-down', randPlayer=True, popsize=20, 
	nwin=0.95)
champ = results['champions'][-1]
for i in range(10):
    print evaluate(champ, task, developer)
print results
#for i in range(n):
#    t=gw()
#    print t.getLoc(2)
#    print t.dispGrid()
#a=gw(copy=t)
#t.move(2)
#t.move(1)
#t.move(1)
#t.move(1)
#t.move(1)
#t.move(1)

#print a.dispGrid()
#print t.dispGrid()
#print t.getLoc(0)
#print t.dispGrid()
#
#print "reward: ", t.getScore()
#t.move(1)
#t.move(1)
#print t.getScore()
#t.move(1)
#
#print t.getScore()
#print "substrate: ",t.getSub()
#print "position can reach: ", t.getActionNode()
#
#outsub = np.zeros(16)
#outsub[12]=1
#print "next position: ", outsub
#t.move2(outsub)
#
#print "new substrate: ",t.getSub()
#print "new position to be reached: ", t.getActionNode()
#print "reward: ", t.getScore()
#print t.getAllLocs()
#print t.getReward()
#print t.dispGrid()