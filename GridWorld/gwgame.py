import numpy as np
from numpy import random

class gw(object):
    def __init__(self, h=4, w=4, npit=1, nwall=1, copy=None, blank=None):
        assert h>=2 and w>=2, "The width and height of grid must be at least 2."
        assert npit+nwall<(h-1)*(w-1), "pit and wall number combined %i exceeds limit %i" %((npit+nwall),
                           (h-1)*(w-1))
        
        
        self.h=h
        self.w=w
        self.npit = npit
        self.nwall = nwall
        self.state = np.zeros((self.h, self.w, 4))
        self.score=0
        self.over=False
        self.win=False
        self._initLocs()
        
        if copy:
            self.copyGW(copy)
        if blank:
            self.state = np.zeros((self.h, self.w, 4))
            
    def copyGW(self, copy):
        '''
        create a new gw instance that copies the copy instance
        '''
        self.h=copy.h
        self.w=copy.w
        self.npit = copy.npit
        self.nwall = copy.nwall
        self.state = np.copy(copy.state)
        self.score=0
        self.over=False
        self.win=False
        
    def geth(self):
        return self.h
    
    def getw(self):
        return self.w
    
    def getLoc(self, obj):
        '''
        return a list of tuples of x, y location
        '''
        if obj == 0:#player
            obj = 3
        elif obj==1:#goal
            obj = 0
        elif obj==2:
            obj=1
        elif obj==3:
            obj=2
        output = []
        for i in range(0,self.h):
            for j in range(0,self.w):
                if (self.state[i,j][obj] == 1):
                    output.append((i,j))
        return output
    
    def getAllLocs(self):
        '''
        return a list of all the object locations
        '''
        locs = self.getLoc(1)+self.getLoc(2)+self.getLoc(3)+self.getLoc(0)
        return locs
    
    def _initLocs(self):
        '''
        initialize locations. player location is set, everything else is randomized.
        '''
        self._setLoc((0,0), 0) #self.h/2, self.w/2
        for i in range(self.npit):
            loc = self.randLoc()
            self._setLoc(loc, 2) #init pit(s)
        for i in range(self.nwall):
            loc = self.randLoc()
            self._setLoc(loc, 3) #init wall(s)
        self._setLoc(self.randLoc(), 1) #init goal
        
    def randOtherLocs(self):
        '''
        randomize locations other than player
        '''
        player = self.getLoc(0)
        self.state = np.zeros((self.h, self.w, 4))
        self._setLoc(player[0], 0)
        for i in range(self.npit):
            loc = self.randLoc()
            self._setLoc(loc, 2)
        for i in range(self.nwall):
            loc = self.randLoc()
            self._setLoc(loc, 3) #init wall(s)
        loc = self.randLoc()
        self._setLoc(loc, 1)

    def _setLoc(self, (x, y), obj, remove=False):
        '''
        takes in a tuple and object number. set self.state.
        '''

        if obj == 0:#player
            obj = 3
        elif obj==1:#goal
            obj = 0
        elif obj==2:#pit
            obj=1
        elif obj==3:#wall
            obj=2
        if remove:
            self.state[x, y][obj]=0
        else:
            self.state[x, y][obj]=1
        if obj==-1:#removeAll
                self.state[x, y] = np.array([0,0,0,0])
                return

    
    def randPloc(self):
        '''
        only change the player location to somewhere random.
        '''
        oldpos = self.getLoc(0)[0]
        self._setLoc(oldpos, -1)
        newpos = self.randLoc()
        self._setLoc(newpos, 0)
        
        
    def randLoc(self, ring=False, bannedpos= None):
        '''
        a helper function that returns a tuple of x, y that is not occupied by any object.
        ring = True:
            x=0 or y=0
        '''
        locs = self.getAllLocs()
        if bannedpos is not None:
            locs = bannedpos
        if not ring:
            temp = random.randint(0, self.h), random.randint(0, self.w)
            if temp in locs:
                return self.randLoc()
            else:
                return temp
        else:
            if random.randint(4)>2:
                temp = (0, random.randint(self.w-1))
                if temp in locs:
                    return self.randLoc(ring=True)
                else:
                    return temp
            else:
                temp = (random.randint(self.h-1), 0)
                if temp in locs:
                    return self.randLoc(ring=True)
                else:
                    return temp

    def getState(self):
        state=np.array(np.zeros((self.h, self.w, 4)))
        state[:] = self.state[:]
        return state
    
    def move(self, action):
        '''
        up, down, left, right -- 0, 1, 2, 3
        '''
        if not self.over:
            player_loc = self.getLoc(0)[0]
            goal = self.getLoc(1)[0]
            pits = self.getLoc(2)
            walls = self.getLoc(3)
            state = self.getState()
            
            #up (row - 1)
            if action==0:
                new_loc = (player_loc[0] - 1, player_loc[1])
                if (new_loc not in walls):
                    if ((np.array(new_loc) < (self.h,self.w)).all() and (np.array(new_loc) >= (0,0)).all()):
                        self._setLoc(new_loc, 0)
                        self._setLoc(player_loc, -1)
            #down (row + 1)
            elif action==1:
                new_loc = (player_loc[0] + 1, player_loc[1])
                if (new_loc not in walls):
                    if ((np.array(new_loc) < (self.h,self.w)).all() and (np.array(new_loc) >= (0,0)).all()):
                        self._setLoc(new_loc, 0)
                        self._setLoc(player_loc, -1)
            #left (column - 1)
            elif action==2:
                new_loc = (player_loc[0], player_loc[1] - 1)
                if (new_loc not in walls):
                    if ((np.array(new_loc) < (self.h,self.w)).all() and (np.array(new_loc) >= (0,0)).all()):
                        self._setLoc(new_loc, 0)
                        self._setLoc(player_loc, -1)
            #right (column + 1)
            elif action==3:
                new_loc = (player_loc[0], player_loc[1] + 1)
                if (new_loc not in walls):
                    if ((np.array(new_loc) < (self.h,self.w)).all() and (np.array(new_loc) >= (0,0)).all()):
                        self._setLoc(new_loc, 0)
                        self._setLoc(player_loc, -1)
            new_player_loc = self.getLoc(0)[0]
            if (not new_player_loc):
                state[player_loc] = np.array([0,0,0,1])
            #re-place pit
            for pit in pits:
                state[pit[0], pit[1]][1]= 1
            #re-place wall
            for wall in walls:
                state[wall[0], wall[1]][2] = 1
            #re-place goal
            state[goal[0], goal[1]][0]= 1
            self._setReward()
    
    def move2(self, outsub):
        '''
        this is for space navigation on substrate. takes in the output of a HyperNEAT,
        make the move and return the go-to position in a 1d array
        '''
        mask = np.zeros(np.size(outsub))
        togoids = self.getActionNode()
        for i in togoids:
            mask[i]=1
        actsub = mask * outsub
        actid = np.argmax(actsub)
        if self.getSub()[actid] !=4:#if not wall
            loc = self.id2pos(actid)
            self._setLoc(self.getLoc(0)[0], -1) #erace trace
            self._setLoc(loc, 0) #set new location
        
        self._setReward()
        return actid
    
    def _checkWin(self):
        '''
        not using. needs improvement.
        what if the shortest path is blocked by an obstruction?
        right now wining is defined by stepping on to the goal, regardless of steps taken.
        '''
        minus = self.getLoc(0)-self.getLoc(1)
        minus = abs(minus[0])+abs(minus[1])
        if self.getScore >= 10-minus:
            self.win=True
        
    def _setReward(self):
        '''
        get called after move
        '''
        player = self.getLoc(0)[0]
        pit = self.getLoc(2)
        goal = self.getLoc(1)[0]
        if (player in pit):
            self.over=True
            self.score-=10
        elif (player == goal):
            self.over=True
            self.win=True
            self.score+=10
        else:
            self.score-=1

    def getReward(self):
        player = self.getLoc(0)[0]
        pit = self.getLoc(2)
        goal = self.getLoc(1)[0]
        if (player in pit):
            return -10
        elif (player == goal):
            return 10
        else:
            return -1

    def getScore(self):
        return self.score
    
    def isover(self):
        return self.over


    def dispGrid(self):
        grid = np.zeros((self.h,self.w), dtype='<U2')
        player_loc=None
        goal=None
        if len(self.getLoc(0))!=0:
            player_loc = self.getLoc(0)[0]
        for i in range(self.nwall):
            wall = self.getLoc(3)
        if len(self.getLoc(1))!=0:
            goal = self.getLoc(1)[0]
        for i in range(self.npit):
            pit = self.getLoc(2)
        for i in range(0,self.h):
            for j in range(0,self.w):
                grid[i,j] = ' '
    
        if player_loc:
            grid[player_loc] = 'P' #player
        if wall:
            for w in wall:
                grid[w] = 'W' #wall
        if goal:
            grid[goal] = '+' #goal
        if pit:
            for p in pit:
                grid[p] = '-' #pit
        return grid
        
    def getSubid(self, (x, y)=(-1, -1), obj=0):
        '''
        convert the object's position to a single index
        e.g: (1, 1) in a 4x4 grid is 5
        or convert x, y to a single index
        '''
        if (x, y) != (-1, -1):
            x, y = x, y
        else:
            x, y = self.getLoc(obj)[0]
        return x*self.h + y
    
    def id2pos(self, id):
        '''
        convert a single index to x, y
        '''
        return (id//self.h, id%self.w)
    
    def getSub(self):
        '''
        convert the state, a 3-d array, to a 1-d array
        '''
        sub = np.zeros(self.h*self.w)
        sub[self.getSubid((self.getLoc(0)[0]))]=1 #set player node on substrate
        sub[self.getSubid((self.getLoc(1)[0]))]=2 #set goal
        for i in self.getLoc(2):
            sub[self.getSubid(i)]=3 #set pit
        for i in self.getLoc(3):
            sub[self.getSubid(i)]=4 #set wall
        return sub
    
    def getActionNode(self):
        '''
        Get an array list of movable position
        e.g player at (0,0) has movable position [(0, 1), (1, 0)]
        '''
        out = []
        pid = self.getSubid(obj=0)
        if pid>self.w: #if pid larger than width, hence can move up
            out.append(pid-self.w)
        if pid<self.w * (self.h-1): #if pid smaller than width * (height-1)
            out.append(pid+self.w)
        if pid>0: # can move to left
            out.append(pid-1) # can move to right
        if pid<self.w * self.h -1:
            out.append(pid+1)
        return np.array(out)
    