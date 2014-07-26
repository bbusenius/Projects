"""
Mini-max Tic-Tac-Toe Player
"""

#import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
#import codeskulptor
#codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

# Lookup dictionary for memoization
LOOKUP = {}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """  
    # Base case
    winner = board.check_win()
    if winner != None:
        return SCORES[winner], (-1, -1)
    # Recursive case
    else:

        # Initialize best score and best move variables
        # based on which player it is
        if player == provided.PLAYERX:
            best_score = float("-inf")
        elif player == provided.PLAYERO:
            best_score = float("inf")
        best_move =  (-1, -1)

        # 1. Look at the current game state and get the possible moves.
        # 2. Loop over the possible moves. For each possible move implement 
        # a depth first search using recursion.
        for move in board.get_empty_squares():
            clone = board.clone()
            clone.move(move[0], move[1], player)
            
            
            # -------- Without memoization --------
            #values = mm_move(clone, provided.switch_player(player))

            # -------- Attempt memoization --------
            if clone.__str__() in LOOKUP:
                values = LOOKUP[clone.__str__()]
            else:
                # Call function recursively 
                values = mm_move(clone, provided.switch_player(player))
                LOOKUP[clone.__str__()] = values[0], move
       
            # -------- Non-math solution --------            

            # Maximizing player
            #if player == provided.PLAYERX:
            #    if values[0] == SCORES[provided.PLAYERX]:
            #        return values[0], move
            #    if values[0] > best_score:
            #        best_score = values[0]
            #        best_move = move
            # Minimizing player
            #elif player == provided.PLAYERO:
            #    if values[0] == SCORES[provided.PLAYERO]:
            #        return values[0], move
            #    if values[0] < best_score:
            #        best_score = values[0]
            #        best_move = move

            # -------- Funky math solution uning negamax --------

            # Exit immediately if the next score is a winning score.
            # We can't do any better than this.
            if SCORES[player] == values[0]:
                return values[0], move

            # Update the best score and best move variables
            if values[0] * SCORES[player] > best_score * SCORES[player]:
                best_score = values[0]
                best_move = move

        # 4. Return the score and move with the minimum or maximum value 
        # depending on which player's turn it is. If the game is over and
        # there aren't anymore moves, the final move should be (-1, -1).
        return best_score, best_move 

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

import poc_ttt_minimax_testsuite as unit_test
unit_test.test_mm_move(mm_move)
