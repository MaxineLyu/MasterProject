from __future__ import division
from IPython.display import clear_output
import random
from gwgame import gw
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
import numpy as np
import time
from time import localtime, strftime

class dqnt(object):
    def __init__(self, gwgame, randPlayer=False, randAll=False, buffersize = 180, 
                 batchsize=140, epsilon =1, gamma=0.975, epochs = 50, test_num = 100,
                 steps = 100, clock=None, fitThreshold = 1, stepThreshold = 40):
        self.game = gwgame
        self.randPlayer = randPlayer
        self.randAll = randAll
        self.inputSize = self.game.h * self.game.w * 4
        self.bufferSize = buffersize
        self.batchSize = batchsize
        self.epsilon = epsilon
        self.test_num = test_num
        self.gamma = gamma
        self.epochs = epochs
        self.replay = []
        self.steps = steps
        self.trainStep = 0
        self.clock = clock
        self.fitThreshold = fitThreshold
        self.stepThreshold = self.game.w + self.game.h

        self.accuracyList = []
        self.QmapList = []
        self.timeList = []
        self.lossList = []

        self.h=0

        self.tempGame = self._initGame()
        self.model = self._initModel()

        if not (self.randPlayer or self.randAll):
            self.test_num = 1

    def _initModel(self):
        model = Sequential()
        model.add(Dense(164, init='lecun_uniform', input_shape=(self.inputSize,)))
        model.add(Activation('relu'))
        # model.add(Dropout(0.5)) 

        model.add(Dense(150, init='lecun_uniform'))
        model.add(Activation('relu'))
        # model.add(Dropout(0.5))

        model.add(Dense(4, init='lecun_uniform'))
        model.add(Activation('linear')) #linear output so we can have range of real-valued outputs

        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)#reset weights of neural network4

        return model

    
    def _initGame(self):
        '''
        return an independent, randomized game
        '''
        g=gw(copy=self.game)
        if self.randPlayer:
            g.randPloc()
        elif self.randAll:
            g.randOtherLocs()
        return g

    def test(self, verbose = False):
        count = 0
        for _ in range(self.test_num):
            count+=self.singleTest(verbose = verbose)
        avg = count/self.test_num
        return avg


    def getQmap(self):
        '''
        display q value
        '''
        g=gw(copy=self.game)
        grid = np.zeros((g.h,g.w), dtype='<U2')
        for x in range(g.h):
            for y in range(g.w):
                g._setLoc(g.getLoc(0)[0], 0, remove=True) #remove player
                g._setLoc((x, y), 0)
                grid[x, y] = np.argmax(self.model.predict(
                    g.getState().reshape(1, g.h * g.w *4),
                    batch_size = 1))
        return grid


    def singleTest(self, verbose = False):
        i=0
        g=self._initGame()
        if verbose:
            print("Initial State:")
            print(g.dispGrid())
        #while game still in progress
        while(not g.over):
            state=g.getState()
            qval = self.model.predict(state.reshape(1,self.inputSize), batch_size=1)
            action = (np.argmax(qval)) #take action with highest Q-value
            if verbose:
                print('Move #: %s; Taking action: %s' % (i, action))
            g.move(action)
            if verbose:
                print(g.dispGrid())
            reward = g.getReward()
            if reward != -1:
                if verbose:
                    print("Reward: %s" % (reward,))
                if reward == 10:
                    return True
                else:
                    return False
            i += 1 #If we're taking more than 10 actions, just stop, we probably can't win this game
            if (i > self.stepThreshold):
                if verbose:
                    print("Game lost; too many moves.")
                return False


    def step(self):
        '''
        step the tempGame and append/rewrite buffer with
        (state, action, reward, new_state)
        '''
        self.h+=1
        self.trainStep+=1
        st=self.stepThreshold
        if not (self.randAll or self.randPlayer):
            st *=5
        if self.tempGame.over or self.trainStep>=st: #restart the game if over
            self.tempGame = self._initGame()
            self.trainStep=0
        state = self.tempGame.getState()
        qval = self.model.predict(state.reshape(1,self.inputSize), batch_size=1)
        if (random.random() < self.epsilon): #choose random action
            action = np.random.randint(0,4)
        else: #choose best action from Q(s,a) values
            action = (np.argmax(qval))
        print self.tempGame.dispGrid()
        self.tempGame.move(action)
        new_state = self.tempGame.getState()
        reward = self.tempGame.getReward()
        if self.epsilon > 0.1: #decrement epsilon over time
            self.epsilon -= (1/self.epochs)

        return (state, action, reward, new_state)

    def trainDeter(self, load, epoch_num):
        state, action, reward, new_state = load
        old_qval = self.model.predict(state.reshape(1, self.inputSize))
        new_qval = self.model.predict(new_state.reshape(1, self.inputSize))
        maxQ = np.max(new_qval)
        y = np.zeros((1,4))
        y[:] = old_qval[:]
        if reward == -1: #non-terminal state
            update = (reward + (self.gamma * maxQ))
        else: #terminal state
            update = reward
        y[0][action] = update #only change the corresponding action value
        
        print("Game #: %s" % (epoch_num,))
        hist = self.model.fit(state.reshape(1, self.inputSize), 
            y, batch_size=1, nb_epoch=1, verbose=1)
        clear_output(wait=True)

        return hist.history['loss'][0]
   

    def train(self, epoch_num):
        '''
        sample buffer and train the model
        '''
        if self.randAll or self.randPlayer:
            minibatch = random.sample(self.replay, self.batchSize)
            X_train = []
            y_train = []
            for memory in minibatch:
                old_state, action, reward, new_state = memory
                old_qval = self.model.predict(old_state.reshape(1,self.inputSize), batch_size=1)
                newQ = self.model.predict(new_state.reshape(1,self.inputSize), batch_size=1)
                maxQ = np.max(newQ)
                y = np.zeros((1,4))
                y[:] = old_qval[:]
                if reward == -1: #non-terminal state
                    update = (reward + (self.gamma * maxQ))
                else: #terminal state
                    update = reward
                y[0][action] = update #only change the corresponding action value
                X_train.append(old_state.reshape(self.inputSize,))
                y_train.append(y.reshape(4,))

            X_train = np.array(X_train)
            y_train = np.array(y_train)
            print("Game #: %s" % (epoch_num,))
            hist = self.model.fit(X_train, y_train, batch_size=self.batchSize, 
                nb_epoch=1, verbose=1)
            clear_output(wait=True)

        return hist.history['loss'][0]
    
    def saveModel(self):
        tosave = self.model.to_json()
        name = strftime("DQNmodel"+"%d%b%Y-%H%M%S", localtime())
        with open (name+".json", "w") as f:
            f.write(tosave)
        self.model.save_weights(name+".h5")
        f.close()

    def run(self):
        '''
        define the main logic and record results
        '''
        #fill the buffer
        if self.randAll or self.randPlayer:
            while (len(self.replay) <= self.bufferSize):
                self.replay.append(self.step())
        
        #start the training
        for i in range(self.epochs):
            time0 = time.time()
            lossPerEpoch=[]
            self.trainStep=0
            
            for _ in range(self.steps):
                load = self.step()
                if self.randPlayer or self.randAll:
                    self.replay[self.h % self.bufferSize] = load
                    loss = self.train(i)
                else:
                    loss=self.trainDeter(load, i)
                
                lossPerEpoch.append(loss)
            
            
            avga = self.test()
            time1 = time.time()-time0
            self.timeList.append(time1)
            self.QmapList.append(self.getQmap())

            self.accuracyList.append(avga)

            self.lossList.append(sum(lossPerEpoch)/len(lossPerEpoch))
            dic = {'accuracyList':self.accuracyList,'QmapList':self.QmapList, 
        'timeList':self.timeList, 'lossList':self.lossList, 'solved':False}
            
            if self.clock is not None and self.timeList[-1] >= self.clock:
                self.saveModel()
                return dic

            if avga >= self.fitThreshold and self.fitThreshold is not None:
                dic['solved']=True
                self.saveModel()
                return dic

        self.saveModel()
        if self.fitThreshold is None:
            dic['solved'] = avga>=1
        
        return dic
        
