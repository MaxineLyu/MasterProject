from __future__ import division
from gwgame import gw
from peas.networks.rnn import NeuralNetwork
import numpy as np

class gwt(object):
    def __init__(self, gwgame, trails=100, randPlayer=False, randAll=False, nwin=0.95):
        self.trails = trails
        self.randPlayer = randPlayer
        self.randAll = randAll
        self.game = gwgame
        self.nwin = nwin
        if nwin is None:
            self.nwin=1
        self.developer = None
        self.substrate = None
        if not (self.randPlayer or self.randAll):
            self.trails = 1
    
    def _initGame(self):
        '''
        initialize the game
        '''
        if self.randPlayer:
            self.game.randPloc()
        elif self.randAll:
            self.game._initLocs(randAll=True)
        
    def evaluate(self, network):
        if not network.sandwich:
            raise Exception("This task should be performed by a sandwich net.")
        score = 0
        win= 0
        for i in range(self.trails):
            self._initGame()
            t=gw(copy=self.game)
#            print self.game.dispGrid()
            step = 0
            trace=[]
            trace.append(t.getLoc(0)[0])
            while (not t.isover()) and step<50: #break when game is over or step>=50
                step += 1
                sub = t.getSub()
                network.flush()
                output = network.feed(sub, add_bias=False) #network!
                actid = t.move2(output)
                trace.append(actid)

            if t.win:
                win+=1
            score += t.getScore()
        score = score/self.trails
        win = win/self.trails
#        fitness = win
#        print "average fitness through trail: {}".format(fitness)
#        print "average win through trail: {}".format(win)
        return {'fitness': win, 'score': score}
            
    def solve(self, network):
        return self.evaluate(network)['fitness'] >=self.nwin


            