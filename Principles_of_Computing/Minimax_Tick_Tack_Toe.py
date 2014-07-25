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

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """ 
    # Define the minimizing and maximizing players
    max_player = provided.PLAYERX
    min_player = provided.PLAYERO  

    # Base case
    winner = board.check_win()
    if winner != None:
        score = SCORES[winner]
        return score, (-1, -1)
    # Recursive case
    else: 

        best_scores = []
        best_moves =  []

        # 1. Look at the current game state and get the possible moves.
        moves = board.get_empty_squares()

        # 2. Loop over the possible moves. For each possible move implement 
        # a depth first search using recursion.
        for move in moves:
            board = board.clone()
            board.move(move[0], move[1], player)

            # Call function recursively 
            values = mm_move(board, player)

            best_scores.append(values[0])
            best_moves.append(move)

        
        if player == max_player:
            best_score = max(best_scores)
            best_move = best_moves[best_scores.index(best_score)]
        elif player == min_player:
            best_score = min(best_scores)
            best_move = best_moves[best_scores.index(best_score)]


        # Player that has the next turn
        player = provided.switch_player(player) 

        # 4. Return the score and move with the minimum or maximum value 
        # depending on which player's turn it is. If the game is over and
        # there aren't anymore moves, the final move should be (-1, -1) as
        # a convention.
        #print "TEST", best_score, best_move 
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

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

import poc_ttt_minimax_testsuite as unit_test
unit_test.test_mm_move(mm_move)
