
import copy, time, random

from connect4ai import * # import all of our AI classes

class GameGrid:
    """ The GameGrid class represents a particular state of the Connect4 game board at a 
        specific moment in time.  A new grid object is created after each move."""

    PLAYER_CHARS = ['X','O']  # kind of like a static field in Java (belongs to the class, not individual instances)

    @classmethod  # kind of like a static method in Java (belongs to the class, not individual instances)
    def getOpponentChar(cls,playerChar):
        return cls.PLAYER_CHARS[1 - cls.PLAYER_CHARS.index(playerChar)]
    
    def __init__(self, data):
        # we always create a new (deep) copy of the data for the grid, so that changes 
        # made to this grid don't affect other grids
        self.data = copy.deepcopy(data) 
        self.numRows = len(data)
        self.numCols = len(data[0])
    
    def display(self):
        for row in self.data[::-1]: #iterate row of grid in reverse to print top row first
            print("|" + "|".join(row) + "|")  
            print("-" * (2 * len(row) + 1))   # fancy grid with - and | box edges
        colIndices = [str(c) for c in range(self.numCols)]
        print(" " + " ".join(colIndices) + " ")  
        print()
    
    def checkColumnFull(self,columnNum):
         # is the final row of the specified column not empty?
        return self.data[-1][columnNum] != ' '
        
    def getNonFullColumnIndices(self):
        """ returns the indices of the columns that aren't full (i.e. valid to play in)"""
        return [c for c in range(self.numCols) if not self.checkColumnFull(c)]
        
    def checkAllColumnsFull(self):
        """ returns True if there is no column left to play """
        return ' ' not in self.data[-1]

    def newGridAfterMove(self,playerChar,columnToPlayIn):
        """ returns a new GameGrid object representing the result of 
            the given player choosing to play in the specified column."""
        newGrid = GameGrid(self.data)
        # start from the bottom row, and place the player's marker 
        # in the first empty cell in the specified column
        for row in range(newGrid.numRows):
            if newGrid.data[row][columnToPlayIn] == ' ':
                newGrid.data[row][columnToPlayIn] = playerChar
                return newGrid
    
    def getMarkerAtLocation(self,r,c):
        """returns the player character marker at the specified row and column,
           or ' ' (space) if the palce is empty OR '' if it's outside the grid's bounds.
           NOTE: Unlike Python's usual negative list indexing, this function treats
                  negative indices as "out of bounds"."""
        if r < 0 or r >= self.numRows or c < 0 or c >= self.numCols:
            return ''
        else:
            return self.data[r][c]
            
    def getRowStrings(self):
        """ returns a list of strings representing the data in each row """
        return ["".join(row) for row in self.data]
        
    def getColumnStrings(self):
        """ returns a list of strings representing the data in each column """
        colStrings = []
        for c in range(self.numCols):
            colData = [self.data[r][c] for r in range(self.numRows)]
            colStrings.append("".join(colData))
        return colStrings
        
    def getDiagonalStrings(self):
        """ returns a list of strings representing the data along every diagonal"""
        diagStrings = []
        for diag in range(-self.numCols+1,self.numRows):
            diagData = [self.getMarkerAtLocation(x+diag,x) for x in range(max(self.numRows,self.numCols))]
            diagStrings.append("".join(diagData))
        for diag in range(-self.numCols,self.numRows-1):
            diagData = [self.getMarkerAtLocation((self.numCols-x)+diag,x) for x in range(max(self.numRows,self.numCols))]
            diagStrings.append("".join(diagData))
        return diagStrings
        
    def getAllDirectionStrings(self):
        """ returns a list of strings representing the data along all rows, columns, and diagonals"""
        # Optimization Note: because it's expensive to calculate all these strings, we'll use the idea of
        #    "memoization" (https://en.wikipedia.org/wiki/Memoization) to save the calculated value
        #    the 1st time the function is called, and then every later call quickly returns that saved value.
        if hasattr(self,'allStringsCached'):
            return self.allStringsCached
        else:
            self.allStringsCached = self.getRowStrings() + self.getColumnStrings() + self.getDiagonalStrings()
            return self.allStringsCached
                
    def checkIfPlayerWon(self,playerChar):
        """ returns True if the specified playerChar has won by connecting 4 in a line, and False otherwise."""
        winningPattern = playerChar * 4  # Python note:  "X" * 4 = "XXXX"
        numFourStreaks = sum(s.count(winningPattern) for s in self.getAllDirectionStrings())
        return numFourStreaks > 0
        
    def checkGameOver(self):
        """ returns True if the game is over either by someone winning or by a draw/tie/cat's game"""
        return self.checkAllColumnsFull() \
            or self.checkIfPlayerWon(type(self).PLAYER_CHARS[0]) \
            or self.checkIfPlayerWon(type(self).PLAYER_CHARS[1])
        
    
class HumanPlayer:
    """ Human-controlled player enters their action choice via keyboard console. """
    def __init__(self, playerChar):
        self.playerChar = playerChar
        
    def chooseMove(self,grid):
        print("Human Player " + self.playerChar + "'s turn. ", end="")
        choice = int(input("Choose a column (0-%s) to play next:"%(grid.numCols-1)))
        validChoices = grid.getNonFullColumnIndices()
        while choice not in validChoices:
            choice = int(input("Choose a column to play next:"))
        return choice
        

def makeEmptyGrid(numRows, numCols):
    return GameGrid([[' ' for c in range(numCols)] for r in range(numRows)])


def choosePlayers():
    players = []
    while len(players) < 2:
        playerChar = GameGrid.PLAYER_CHARS[len(players)]
        print("Choose the type of player for player %s (%s):"%(len(players)+1,playerChar))
        print(" 1. Human")
        print(" 2. Random AI")
        print(" 3. MiniMax AI")
        choice = input()
        if choice == '1':
            players.append(HumanPlayer(playerChar))
        elif choice == '2':
            players.append(RandomAIPlayer(playerChar))
        elif choice == '3':
            depth = input("Choose a search depth between 1 ply and whatever your computer can handle: ")
            try:
                players.append(MiniMaxAIPlayer(playerChar, int(depth)))
            except:
                print("Invalid search depth. Choose player type again.")
        else:
            print("Invalid choice.  Try again.")
    return players
            
    
def main():
    """ main function that runs the game! """
    grid = makeEmptyGrid(6,7)
    players = choosePlayers()
    
    currentPlayerIndex = 0
    
    while not grid.checkGameOver():
        print("\n\n")
        grid.display()
        actionColumnChoice = players[currentPlayerIndex].chooseMove(grid)
        grid = grid.newGridAfterMove(GameGrid.PLAYER_CHARS[currentPlayerIndex],actionColumnChoice)
        currentPlayerIndex = 1 - currentPlayerIndex # switch to the other player

    grid.display()

    if grid.checkIfPlayerWon(GameGrid.PLAYER_CHARS[0]):
        print(GameGrid.PLAYER_CHARS[0], "Wins!")
    elif grid.checkIfPlayerWon(GameGrid.PLAYER_CHARS[1]):
        print(GameGrid.PLAYER_CHARS[1], "Wins!")
    else:
        print("The game was a draw.")
    print("Total A.I. search nodes created: ", GameState.totalNodesCreated)
    
    
if __name__ == '__main__':
    main()

