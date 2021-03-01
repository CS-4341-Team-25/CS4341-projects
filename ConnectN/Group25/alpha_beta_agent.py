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
    # def __init__(self, name, max_depth):
    #     super().__init__(name)
    #     # Max search depth
    #     self.max_depth = max_depth
    #     self.count = 0
    #     self.metrics = Metrics()

    def __init__(self, name, max_depth, weight_self_potential = 3, weight_enemy_potential = 0, weight_in_a_row = 1, multiplier_growth_rate = 1, weight_token_height = 1):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.count = 0
        self.weight_self_potential = weight_self_potential # weight for how many potential in-a-rows we have
        self.weight_enemy_potential = weight_enemy_potential # weight for how many potential in-a-rows enemy has
        self.weight_in_a_row = weight_in_a_row # weight for how many in-a-rows we have
        self.multiplier_growth_rate = multiplier_growth_rate # weight for how quickly we increase score for potential n-in-a-rows found
        self.weight_token_height = weight_token_height # weight for height of token (how many rows above row 0 it is)
        print((self.weight_self_potential, self.weight_enemy_potential, self.weight_in_a_row, self.weight_token_height, self.multiplier_growth_rate))
    
    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        cols = brd.free_cols()
        choice = self.alphabeta_decision(brd)

        return choice
    
    # ALPHABETA Algorithm 
    #
    # PARAM [board.Board]
    # RETURN [int]: the column where the token must be added
    def alphabeta_decision(self, brd): 
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
        return bestCol

    # Minimax Algorithm: DO NOT CALL ME
    #
    # PARAM [board.Board]
    # RETURN [int]: the column where the token should be added
    # def minimax_decision(self, brd): 
    #     self.metrics.start_timer()
    #     bestScore = float('-inf')
    #     bestCol = 0
    #     # get board with maximum score 
    #     for newBrd,newCol in self.get_successors(brd):
    #         nextScore = self.min_value(newBrd)
    #         if nextScore > bestScore:
    #             bestScore = nextScore
    #             bestCol = newCol
    #     elapsed_time = self.metrics.end_timer()
    #     return bestCol

    # Maximizer function for alpha beta algorithm
    #
    # PARAM [board.Board]
    # PARAM alpha 
    # PARAM beta
    # PARAM depth   Current depth
    def max_value(self, brd, alpha, beta, depth):
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
    
    # Minimizer function for alpha beta algorithm
    #
    # PARAM [board.Board]
    # PARAM alpha 
    # PARAM beta
    # PARAM depth   Current depth
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

    # Assigns a score of a terminal state: win, loss, tie 
    def utility(self, brd):
        # determine how many pieces we have played 
        i = 0
        for row in brd.board:
            for elem in row:
                if elem != 0:
                    i+=1
        
        pieces_played = i/2
        
        # scoring function
        utility = brd.w * brd.h - pieces_played

        # if there is no winner, tie, return 0
        if brd.get_outcome() == 0:
            utility = 0
        # if there is a winner, and its not us, return -1 * utility
        elif brd.get_outcome() != self.player:
            utility = -utility

        # always weight utility score higher than heuristic-generated score 
        return utility*1000

    # Heuristic function to use for scoring configurations for moves greater than max_depth
    def heuristic(self, brd):
        enemy = 1
        if self.player == 1:
            enemy = 2
        
        factor_self_potential =  self.get_potential_wins(brd, self.player)
        factor_enemy_potential = self.get_potential_wins(brd, enemy)

        h = self.weight_self_potential * factor_self_potential -  self.weight_enemy_potential * factor_enemy_potential
        return h

    # Returns the potential wins of a player on a given board based on the number of 1, 2, and 3 in-a-rows.
    # PARAM brd:    The board being evaluated
    # PARAM player: The player being scored 
    def get_potential_wins(self, brd, player):
        """Return total number of potential wins for us"""
        output = 0
        for x in range(brd.w):
            for y in range(brd.h):
                if (brd.board[y][x] == player): 
                    output += self.any_potential_line_at(brd, player, x,y) # Score each token
        return output

    # Checks if there is a potential line at a given token
    # A potential line is one where there is 1,2, or 3 in-a-row that is not blocked
    # PARAM brd:    The board being evaluated
    # PARAM player: the player being evaluated
    # PARAM x:      the x position of the space being tested
    # PARAM y:      The y position of the space being tested
    def any_potential_line_at(self, brd, player, x, y):
        """Return True if a line of n number of identical tokens are ready to be played starting at (x,y) in any direction"""
        return (self.potential_line_at(brd, player, x, y, 1, 0) or # Horizontal
                self.potential_line_at(brd, player, x, y, 0, 1) or # Vertical
                self.potential_line_at(brd, player, x, y, 1, 1) or # Diagonal up
                self.potential_line_at(brd, player, x, y, 1, -1)) # Diagonal down

    # Calculates if there is a potential line at a given token in a specific direction
    # A potential line is one where there is 1,2, or 3 in-a-row that is not blocked
    # PARAM brd:    The board being evaluated
    # PARAM player: the player being evaluated
    # PARAM x:      the x position of the space being tested
    # PARAM y:      The y position of the space being tested
    # PARAM dx:     The x direction of the line being checked
    # PARAM dx:     The y direction of the line being checked
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
                if (y_pos + 1 < len(brd.board) and brd.board[y_pos + 1][x+i*dx] == 0): # check if the token is foating or if is resting on another
                    token_height += 1          
                linear_growth_rate = 1
                factor_in_a_row = self.multiplier_growth_rate * (factor_in_a_row + linear_growth_rate) # increase the score based on how many are in a row
                
        return self.weight_in_a_row * factor_in_a_row - self.weight_token_height * token_height # return the weighted final value

    
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
        
THE_AGENT = AlphaBetaAgent("Group25", 4)