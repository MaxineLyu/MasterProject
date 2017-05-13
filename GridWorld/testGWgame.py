from gwgame import gw
import numpy as np
from drawGW import *


maps = []
g=gw(h=4, w=4, blank=True)
g._setLoc((0,0),0)
g._setLoc((0,1),3)
g._setLoc((2,1),3)
g._setLoc((2,2),3)
g._setLoc((0,3),1)
g._setLoc((1,2),2)
print g.dispGrid()
maps.append(g)
g=gw(h=4, w=4, blank=True)
g._setLoc((0,3),2)
g._setLoc((1,2),0)
g._setLoc((1,1),3)
g._setLoc((2,1),3)
g._setLoc((2,2),3)
g._setLoc((0,0),1)
print g.dispGrid()
maps.append(g)
size=10


maps.append(g)


size=7
g=gw(h=size, w=size, blank=True)
drawStripeMap(size, size, g)
print g.dispGrid()
print g.state[size/2, size/2]