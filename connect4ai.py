## NOTE: Look for the "TODO:" comments below


import math # so we can use math.inf and -math.inf (positive and negative infinity)
import time, random

class GameState:
    """ this class encapsulates both the game play grid and whose turn it is at this state,
        and is used to represent nodes in the search tree."""
    totalNodesCreated = 0
    def __init__(self, grid, currentPlayerChar):
        GameState.totalNodesCreated += 1
        self.grid = grid
        self.currentPlayerChar = currentPlayerChar
        # in case the A.I. search doesn't find/set the best action 
        # (e.g. might happen if all actions lead to defeat)
        # we'll initialize it to a random action here
        if (not grid.checkAllColumnsFull()):
            self.bestAction = random.choice(grid.getNonFullColumnIndices())
                
    # Python note: starting a method name with underscore is the Python convention for declaring it "private"
    def _getLegalActions(self):
        return self.grid.getNonFullColumnIndices()

    def _getSuccessorForAction(self, columnToPlay):
        return GameState(self.grid.newGridAfterMove(self.currentPlayerChar,columnToPlay),
                            self.grid.getOpponentChar(self.currentPlayerChar))
    
    def getActionsAndSuccessors(self):
        """ returns a list of (action, successor-state) pairs for each action (legal play) 
            that can be taken after this state"""
        return [(action,self._getSuccessorForAction(action)) for action in self._getLegalActions()]

    def setBestAction(self, bestAction):
        """ During the search (at least for the root node), we want to keep track of
            which action led to the best (min or max) value for each min/max search node.
            The minimax search algorithm should update this as it goes."""
        self.bestAction = bestAction
    
    def getBestAction(self):
        """ returns the best action field that should have been found and stored during the search process """
        return self.bestAction
        
    def isTerminal(self):
        """ returns True if this is a 'terminal' game state """
        return self.grid.checkGameOver()
    
    def estimateValueForPlayer(self, playerChar):
        """ returns the actual value (from playerChar's perspective) of this state if it 
            is a terminal state, or a heuristic estimate of the value otherwise."""
        if self.isTerminal():
            if self.grid.checkIfPlayerWon(playerChar):
                return math.inf
            elif self.grid.checkIfPlayerWon(self.grid.getOpponentChar(playerChar)):
                return -math.inf
            else:
                return 0 # tie
        else:
            return self.heuristicValueForPlayer(playerChar)
    
    def heuristicValueForPlayer(self, playerChar):
        """ returns a heuristic value anywhere between -infinity (certain loss) 
            and +infinity (certain win) estimating how good the state is
            for the given playerChar """
        # TODO: Fill in this this method, and return a more informative value
        #       based on self.grid
        return 0


class RandomAIPlayer:
    """ A "stupid" AI player that just plays randomly. """
    def __init__(self, myPlayerChar):
        self.myPlayerChar = myPlayerChar
        
    def chooseMove(self,grid):
        """ returns a random action (column index integer) to take. """
        print("Random AI Player " + self.myPlayerChar + "'s turn... ",end='')
        time.sleep(1)  # have Random pause a sec so viewer has time to see each play
        return random.choice(grid.getNonFullColumnIndices())


class MiniMaxAIPlayer:
    def __init__(self, myPlayerChar, searchDepthLimit):
        self.myPlayerChar = myPlayerChar
        self.searchDepthLimit = searchDepthLimit
        self.totalThinkingTime = 0
        
    def chooseMove(self,grid):
        """ returns the action this AI decides is the best to take """
        print("MiniMax-depth%s AI Player %s's turn:"%(self.searchDepthLimit,self.myPlayerChar))
        startTime = time.clock()
        curState = GameState(grid, self.myPlayerChar)
        val = self.getValueOfState(curState,self.searchDepthLimit,-math.inf,math.inf)
        thinkingTime = (time.clock()-startTime)
        self.totalThinkingTime += thinkingTime  # keep track of how long the AI is taking to move
        print(" (calculating this move took %.3f sec, total thinking time %.2f)"%(thinkingTime,self.totalThinkingTime))
        return curState.getBestAction()

    def getValueOfState(self,gState,depthLimit,alpha,beta):
        """ returns the value (from this A.I. player's perspective) of the given
            GameState object gState.  If the depthLimit parameter is down to zero,
            or if it's a terminal state, then we directly return the (estimated) value
            of the state -- otherwise we call getMaxValue or getMinValue appropriately 
            depending on whether gState's current player char is the same as this
            AI player's current player char... and those methods will recursively 
            call this getValueOfState(...) method on their child (successor) states"""
        if (depthLimit == 0) or (gState.isTerminal(self)):
            return gState.value
        if (self.myPlayerChar == gState.currentPlayerChar):
            return getMaxValue(self,gState,depthLimit,alpha,beta)
        else:
            return getMinValue(self,gState,depthLimit,alpha,beta)
        

    def getMaxValue(self,gState,depthLimit,alpha,beta):
        """ returns the MAXIMUM value that can be achieved among the successor (child) states
            from the given GameState gState.  Importantly, this method also calls the
            gState.setBestAction(...) method to store the action that yielded that maximal value.
            
            For greater efficiency, this method uses alpha-beta pruning."""
        maxVal = alpha
        for successor in gState.getActionsAndSuccessors():
            maxVal = max(maxVal,getMinValue(successor))      
            if (maxVal > self.getBestAction):
                self.setBestAction(maxVal)
        return maxVal

    def getMinValue(self,gState,depthLimit,alpha,beta):
        """ returns the MINIMUM value that can be achieved among the successor (child) states
            from the given GameState gState.  Importantly, this method also calls the
            gState.setBestAction(...) method to store the action that yielded that minimal value.
            
            For greater efficiency, this method uses alpha-beta pruning."""
        minVal = beta
        for successor in gState.getActionsAndSuccessors():        
            minVal = min(minVal,getValueOfState(self,gState,depthLimit,alpha,beta))
            if (minVal < self.getBestAction):
                self.setBestAction(minVal)
        return minVal


        
