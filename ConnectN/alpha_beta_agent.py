import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        cols = brd.free_cols()
        choice = self.minimax_decision(brd)
        return choice
    
    # Minimax Algorithm 
    #
    # PARAM [board.Board]
    # RETURN [int]: the column where the token must be added
    def minimax_decision(self, brd): 
        
        bestScore = float('-inf')
        bestCol = 0
        for newBrd,newCol in self.get_successors(brd):
            nextScore = self.min_value(newBrd)
            if nextScore > bestScore:
                bestScore = nextScore
                bestCol = newCol
        return bestCol

    def max_value(self, brd):
        if (brd.get_outcome() != 0):
            return self.utility(brd)
        v = float('-inf')
        for successor in self.get_successors(brd):
            v = max(v, self.min_value(successor[0]))
            # successor is [list of (board.Board, int)]
        return v

    def min_value(self, brd):
        if (brd.get_outcome() != 0):
            return self.utility(brd)
        v = float('inf')
        for [successor, col] in self.get_successors(brd):
            v = min(v, self.max_value(successor))
        return v

    def utility(self, brd):
        i = 0
        for row in brd.board:
            for elem in row:
                if i != 0:
                    i+=1
        
        pieces_played = i/2

        return brd.w * brd.h - pieces_played

    
    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    #TODO implement some sort of heuristic for move ordering
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
