from DQNtask import *
from gwgame import gw
import numpy as np
import pickle
import drawGW as dgw


def drawCircle(h, w, r):
	y=np.arange(h)
	a=[]
	b=[]
	temp=r**2-(y-h/2)**2
	for i in range(len(temp)):
		if temp[i]>=0:
			x=temp[i]
			x=x**.5+h/2
			x=np.round(x).astype(int)
			a.append((x, y[i]))
			b.append((h-1-x, y[i]))
	for loc in a:
		g._setLoc(loc, 3)
	for loc in b:
		g._setLoc(loc, 3)

size=10
g=gw(h=size, w=size, blank=True)

g = dgw.drawStripe(size, size, g)
g._setLoc((0, 0), 0)
g._setLoc((size-1, size-1), 1)

g=gw(h=7, w=7, npit=3, nwall=3)
t = dqnt(g, randPlayer=False, epochs=50, fitThreshold = 1, stepThreshold = 20)
dic = t.epoch()
print dic

# with open('DQN5000.pickle', 'w') as f:
# 	pickle.dump(model, f)