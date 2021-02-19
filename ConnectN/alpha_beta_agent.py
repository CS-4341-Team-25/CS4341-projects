import math
import agent
from metrics import Metrics

###########################
# Alpha-Beta Search Agent #
###########################
class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    # def __init__(self, name, max_depth):
    #     super().__init__(name)
    #     # Max search depth
    #     self.max_depth = max_depth
    #     self.count = 0
    #     self.metrics = Metrics()

    def __init__(self, name, max_depth, weight_self_potential = 1, weight_enemy_potential = 0, weight_in_a_row = 1, multiplier_growth_rate = 1, weight_token_height = 0):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.count = 0
        self.metrics = Metrics()
        self.weight_self_potential = weight_self_potential # weight for how many potential in-a-rows we have
        self.weight_enemy_potential = weight_enemy_potential # weight for how many potential in-a-rows enemy has
        self.weight_in_a_row = weight_in_a_row # weight for how many in-a-rows we have
        self.multiplier_growth_rate = multiplier_growth_rate
        self.weight_token_height = weight_token_height
        print((self.weight_self_potential, self.weight_enemy_potential, self.weight_in_a_row, self.weight_token_height, self.multiplier_growth_rate))
    
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
        # print("I am think ...")
        choice = self.alphabeta_decision(brd)
        self.print_metrics()
        return choice
    
    # ALPHABETA Algorithm 
    #
    # PARAM [board.Board]
    # RETURN [int]: the column where the token must be added
    def alphabeta_decision(self, brd): 
        self.metrics.start_timer()
        bestScore = float('-inf')
        bestCol = 0
        cols_checked = 0
        for newBrd,newCol in self.get_successors(brd):
            cols_checked += 1
            
            nextScore = self.min_value(newBrd, float('-inf'), float('inf'), 1)
            if nextScore > bestScore:
                bestScore = nextScore
                bestCol = newCol
            # print("Checked " + str(cols_checked) + " node(s)")
        elapsed_time = self.metrics.end_timer()
        return bestCol

    # Minimax Algorithm 
    #
    # PARAM [board.Board]
    # RETURN [int]: the column where the token must be added
    def minimax_decision(self, brd): 
        self.metrics.start_timer()
        bestScore = float('-inf')
        bestCol = 0
        for newBrd,newCol in self.get_successors(brd):
            nextScore = self.min_value(newBrd)
            if nextScore > bestScore:
                bestScore = nextScore
                bestCol = newCol
        elapsed_time = self.metrics.end_timer()
        return bestCol

    # Print statements for measuring metrics for each move and game overall
    def print_metrics(self):
        pass
        # print("Think complete! Max elapsed time: ", self.metrics.max_elapsed)
        # print("Avg nodes/s ", self.metrics.getNodePerSec())
        # print("Avg time per move ", self.metrics.getAvgTimePerMove())
        # print("Moves to win ", self.metrics.moves)
        # print("Total nodes checked: ", self.metrics.total_nodes_checked)

    def max_value(self, brd, alpha, beta, depth):
        #def max_value(self, brd):
        # game is over, it is a terminal state, check utility
        local_alpha = alpha
        local_beta = beta
        if ((len(brd.free_cols()) == 0) or (brd.get_outcome())) != 0:
            return self.utility(brd)
        if (depth > self.max_depth):
            return self.heuristic(brd)
        v = float('-inf')
        for successor, col in self.get_successors(brd):
            v = max(v, self.min_value(successor, local_alpha, local_beta, depth + 1))
            if v >= local_beta:
                return v
            local_alpha = max(local_alpha, v)
            #successor is [list of (board.Board, int)]
        return v

    def min_value(self, brd, alpha, beta, depth):
        # game is over, it is a terminal state, check utility
        local_alpha = alpha
        local_beta = beta
        if (len(brd.free_cols()) == 0 or brd.get_outcome() != 0):
            return self.utility(brd)
        if (depth > self.max_depth):
            return self.heuristic(brd)
        v = float('inf')
        for successor, col in self.get_successors(brd):
            v = min(v, self.max_value(successor, local_alpha, local_beta, depth + 1))
            if v <= local_alpha:
                return v
            local_beta = min(local_beta, v)
        return v


    #TODO make not suck
    def utility(self, brd):
        i = 0
        for row in brd.board:
            for elem in row:
                if elem != 0:
                    i+=1
        
        pieces_played = i/2

        utility = brd.w * brd.h - pieces_played

        # if there is no winner, tie, return 0
        if brd.get_outcome() == 0:
            utility = 0
        # if there is a winner, and its not us, return -1 * utility
        elif brd.get_outcome() != self.player:
            utility = -utility

        self.metrics.count()
        # always weight utility score higher than heuristic-generated score 
        return utility*1000

    def heuristic(self, brd):
        enemy = 1
        if self.player == 1:
            enemy = 2
        
        factor_self_potential =  self.get_potential_wins(brd, self.player)
        factor_enemy_potential = self.get_potential_wins(brd, enemy)

        h = self.weight_self_potential * factor_self_potential -  self.weight_enemy_potential * factor_enemy_potential
        return h

    def get_potential_wins(self, brd, player):
        """Return total number of potential wins for us"""
        output = 0
        for x in range(brd.w):
            for y in range(brd.h):
                if (brd.board[y][x] == player): 
                    output += self.any_potential_line_at(brd, player, x,y)
        return output

    def any_potential_line_at(self, brd, player, x, y):
        """Return True if a line of n number of identical tokens are ready to be played starting at (x,y) in any direction"""
        return (self.potential_line_at(brd, player, x, y, 1, 0) or # Horizontal
                self.potential_line_at(brd, player, x, y, 0, 1) or # Vertical
                self.potential_line_at(brd, player, x, y, 1, 1) or # Diagonal up
                self.potential_line_at(brd, player, x, y, 1, -1)) # Diagonal down

    def potential_line_at(self, brd, player, x, y, dx, dy):
        """Return number of n-in-a-rows that could be played starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (brd.n-1) * dx >= brd.w) or
            (y + (brd.n-1) * dy < 0) or (y + (brd.n-1) * dy >= brd.h)):
            return 0
        # Go through elements
        enemy = 1
        if player == 1:
            enemy = 2
        
        factor_in_a_row = 1
        token_height = 0

        for i in range(1, brd.n): # check for tokens in range n
            if brd.board[y + i*dy][x + i*dx] == enemy:
                return 0
            if brd.board[y + i*dy][x + i*dx] == player:
                y_pos = y+i*dy
                if (y_pos + 1 < len(brd.board) and brd.board[y_pos + 1][x+i*dx] == 0):
                    token_height += 1          
                linear_growth_rate = 1
                factor_in_a_row = self.multiplier_growth_rate * (factor_in_a_row + linear_growth_rate)
                
        return self.weight_in_a_row * factor_in_a_row - self.weight_token_height * token_height

    
    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        def sortFun(e):
            return len(freecols)/2 - e
        freecols.sort(key=sortFun)
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
        
    # To be called by tournament in between games, just for testing / metrics purposes 
    def reset_agent_metrics(self):
        self.metrics.reset_metrics()
