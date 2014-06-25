"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
#import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Play a game of random moves, alternating between players.
    Modify the game state. 

    Args:
        board: object, the current game board.

        player: int, the next player to move.

    Returns:
        None (but alters the game state) 
    """
    print board.get_empty_squares()
    print player

def mc_update_scores(scores, board, player):
    """
    Function scores the completed board and updates the scores grid.

    Args:
        scores: list of lists, with the same dimensions as the Tic-Tac-Toe board

        board: a board from a completed game.

        player: which player the machine player is.

    Return:
        None.
    """
    pass

def get_best_move(board, scores):
    """
    Find all of the empty squares with the maximum score and randomly return one of them as a (row, column) tuple.
    Do not call this function with a board that has no empty squares.

    Args:
        board: current board

        scores: grid of scores

    Returns:
        tuple, a randomly picked empty square with the maximum score.
    """
    pass

def mc_move(board, player, trials):
    """
    Use the Monte Carlo simulation to return a move for the machine player.

    Args:
        board: current board

        player: which player the machine player is

        trials: the number of trials to run.

    Returns:
        tuple, (row, column)
    """
    pass

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
import monte_carlo_testsuite as test_ttt
test_ttt.test_trial(mc_trial)
