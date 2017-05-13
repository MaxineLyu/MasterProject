from gwgame import gw
from drawGW import *
import pickle

StationaryMaps = []

def drawg1(size): #stationary
	g=gw(h=size, w=size, blank=True) # SUPER EASY, LINEAR
	g._setLoc((0,0), 0)
	if size<7:
		small=True
	else:
		small=False
	if small:
		g._setLoc((size-1,0), 1)
		g._setLoc((size/2,size/2+1), 2)
		g._setLoc((0,size/2+1), 3)
	else:
		r=size/2-1
		if size==7:
			r=size/2
		drawCircle(size, size, r, g)
		drawCircle(size, size, 1, g)
		g._setLoc((size/2,size/2+1), 3, remove=True)
		
		g._setLoc((size/2, size/2), 1)
	return g


def drawg2(size):
	g=gw(h=size, w=size, blank=True) # EASY
	g._setLoc((0,0), 0)
	if size<7:
		small=True
	else:
		small=False
	if small:
		g._setLoc((size-1,size-1), 1)
		g._setLoc((size-1,0), 2)
		g._setLoc((0,size-1), 3)
	else:
		drawStripeMap(size, size, g)
		g._setLoc((size-1, size-1), 1)
	return g


def drawg3(size):
	if size<7:
		small=True
	else:
		small=False
	g=gw(h=size, w=size, blank=True) #same as 3rd, obj=5, wall++
	if small:
		g._setLoc((0,0), 0)
		g._setLoc((0,size-1), 1)
		g._setLoc((0,size-2), 3)
		g._setLoc((1,size-2), 3)
		g._setLoc((size/2+1,0), 2)
	else:
		drawVortexMap(size, size, g)
	return g

def drawg4(size):
	if size<7:
		small=True
	else:
		small=False
	g=gw(h=size, w=size, blank=True) #hard, non-linear, obj=4
	if small:
		g._setLoc((0,0), 0)
		g._setLoc((size/2-1,1), 2)
		g._setLoc((size/2,0), 3)
		g._setLoc((size/2+1,0), 1)
	return g

def drawg5(size):
	if size<7:
		small=True
	else:
		small=False
	g=gw(h=size, w=size, blank=True) #goal behind pit, obj=6, pit++
	if small:
		g._setLoc((0,0), 0)
		g._setLoc((size/2+1,0), 1)
		g._setLoc((size/2,0), 3)
		g._setLoc((size/2-1,1), 2)
		g._setLoc((size/2-1,2), 2)
	return g

map46 = []
map710 =[]	
for size in range(4, 7):
	print "size", size
	h, w = size, size
	print "g1"
	g1=drawg1(size)
	print "g2"
	g2=drawg2(size)
	print "g3"
	g3=drawg3(size)
	print "g4"
	g4=drawg4(size)
	print "g5"
	g5=drawg5(size)
	map46=map46 + [g1]+[g2]+[g3]+[g4]+[g5]


for size in range(7, 11):
	print "size", size
	h, w = size, size
	print "g1"
	g1=drawg1(size)
	print "g2"
	g2=drawg2(size)
	print "g3"
	g3=drawg3(size)
	map710= map710+[g1]+[g2]+[g3]

maps = map46+map710

for i in maps:
	print i.dispGrid()
print len(maps)
# with open('maps.pickle', 'w') as f:
# 	pickle.dump(maps, f)