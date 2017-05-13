from gwgame import gw
import numpy as np

def drawCircle(h, w, r, g):
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
	return g

def drawCircleMap(h, w, g):
	#unfinished
	r=h/2
	if h%2 == 0:
		r-=1
	g.drawCircle(h, w, r, g)

def drawStripeMap(h, w, g):
	switch = False
	for y in range(w):
		if y % 2 != 0:
			if switch:
				g._setLoc((2, y), 2) #set pit
				for x in range(3, h): #from 3rd to the end
					g._setLoc((x, y), 3)
			else:
				g._setLoc((h-3, y), 2) #set pit
				for x in range(0, h-3): #from 3rd to the end
					g._setLoc((x, y), 3)

			switch = not switch
	return g


def drawSquare(g, topleft = (0,0), length=1, width=1):
	x0, y0 = topleft
	for y in range(y0, y0+width):
		g._setLoc((x0, y), 3)
		g._setLoc((x0+length-1, y), 3)
	for x in range(x0, x0+length):
		g._setLoc((x, y0), 3)
		g._setLoc((x, y0+width-1), 3)
	return g


def drawVortexMap(h, w, g, switch=False):
	side=h
	x0, y0 = 0,0
	startx, starty= 0, 1
	if switch:
		startx, starty = 1, 0
	
	g._setLoc((startx, starty), 0)
	
	while side>0 and x0<h/2:
		drawSquare(g, length=side, width = side, topleft = (x0, y0))
		side -= 4
		x0+=2
		y0+=2
		g._setLoc((startx, starty), 3, remove=True)
		startx+=2
		starty+=2
		if switch:
			g._setLoc((startx-1, starty-1), 3)
		else:
			g._setLoc((startx-1, starty-1), 3)
	g._setLoc((h/2, w/2), 1)
	g._setLoc((h/2, w/2), 3, remove=True)
	return g
	