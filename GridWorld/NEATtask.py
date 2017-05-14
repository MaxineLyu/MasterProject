from __future__ import division
from peas.networks.rnn import NeuralNetwork
import numpy as np
np.set_printoptions(threshold=np.nan)
from gwgame import gw as gwg


class gwt(object):
    def __init__(self, gw, trails=100, randPlayer=False, randAll=False, nwin=None):
        self.game = gw
        self.h=gw.h
        self.w=gw.w
        self.npit=gw.npit
        self.nwall=gw.nwall
        self.trails = trails
        self.randPlayer = randPlayer
        self.randAll = randAll
        self.nwin=nwin
        if nwin is None:
            self.nwin=1
        if not (randPlayer or randAll) is True:
            self.trails=1
        print gw.dispGrid()
    
    def _initGame(self):
        if self.randPlayer:
            return self.game.randPloc()
        elif self.randAll:
            return self.game._initLocs()
        return self.game
    
    def getGame(self):
        return self.game
        
    def evaluate(self, network):#deterministic
        if not isinstance(network, NeuralNetwork):
            network = NeuralNetwork(network)
        score = 0
        win= 0
        for i in range(self.trails):
            t = gwg(copy=self._initGame()) #
            step = 0
            trace=[]
            trace.append(t.getLoc(0)[0])
            while (not t.isover()) and step<50: #break when game is over or step>=50
                step += 1
                sub=t.getSub()
                output = network.feed(sub)[-4:]
                t.move(np.argmax(output)) #make move
#                trace.append(np.argmax(output))
#            print trace
            if t.win:
                win+=1
#                print "win"
            score += t.getScore()
        score = score/self.trails
        win = win/self.trails
        if self.randPlayer or self.randAll:
            return {'fitness':win, 'score':score, 'win':win}
#        fitness = win
#        print "average fitness through trail: {}".format(fitness)
#        print "average win through trail: {}".format(win)
        return {'fitness': score, 'win': win, 'score':score}
            
    def solve(self, network):
        if not isinstance(network, NeuralNetwork):
            network = NeuralNetwork(network)
        print self.nwin
        print self.evaluate(network)['win']
        return self.evaluate(network)['win'] >= self.nwin
    