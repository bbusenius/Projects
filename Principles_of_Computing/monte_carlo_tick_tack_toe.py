"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
#import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 500    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player

# Lookup by winner, tie, or empty in the dictionsry 
# 1 is empty, 2 is oppoent, 3 is player, 4 is a tie
# Within each dictionary lookup by the player who 
# "owns" the square. 1 is empty, 2 is the opponent, 
# 3 is the current player.
SQUARE_SCORE = {1 : {3 : 0.0, 2 : 0.0, 1 : 0.0 },
                2 : {3 : -MCMATCH, 2 : MCOTHER, 1 : 0.0},
                3 : {3 : MCMATCH, 2 : -MCOTHER, 1 : 0.0},
                4 : {3 : 0.0, 2 : 0.0, 1 : 0.0}}
    
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

    # Get all empty sqares on the board 
    empty_squares = board.get_empty_squares()

    # Randomly select an empty square
    for dummy_move in range(len(empty_squares)): 
        square = random.choice(empty_squares)
        
        # Player makes a move 
        board.move(square[0], square[1], player)

        # Remove a square after using it
        empty_squares.remove(square)

        # Switch players 
        player = provided.switch_player(player)

        # Stop the game if there's a winner
        if board.check_win(): 
            break

    return None

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
    winner = board.check_win()
    # Loop through the grid and update the scores grid by doing a dictionary lookup.
    # Lookup by winner > player to get the correct score for each square.
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            player = board.square(row, col)
            score = SQUARE_SCORE[winner][player] 
            scores[row][col] += score
    return scores

def get_best_move(board, scores):
    """
    Find all of the empty squares with the maximum score and randomly return one of them as a (row, column) tuple.
    Do not call this function with a board that has no empty squares.

    Args:
        board: current board

        scores: grid of scores

    Returns:
        tuple, a randomly picked empty square with the maximum score. 
        Returns None if there aren't any empty squares left.
    """
    # Get all empty sqares on the board
    empty_squares = board.get_empty_squares() 

    # Find the highest score. 
    highest_score = float('-inf')
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            coordinates = (row, col)
            if coordinates in empty_squares and scores[row][col] > highest_score:
                highest_score = scores[row][col]
   
    # Get the grid coordinates of all 
    # squares with the highest score.
    highest_scores = []
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            coordinates = (row, col)
            if coordinates in empty_squares and scores[row][col] == highest_score:
                highest_scores.append((row, col))
    return random.choice(highest_scores)

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
    # Clone the board to use for monte carlo practice games 
    # and setup a list of null scores. 
    scores = [[0] * board.get_dim()] * board.get_dim()

    # Leave the function if there is no next move
    if board.check_win():
        return None

    for dummy_game in range(trials):
        clone = board.clone()
        mc_trial(clone, player)
        mc_update_scores(scores, clone, player)
    return get_best_move(board, scores)
        

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
#import monte_carlo_testsuite as test_ttt
#test_ttt.test_trial(mc_trial)
#test_ttt.test_update_scores(mc_update_scores, MCMATCH, MCOTHER)
#test_ttt.test_best_move(get_best_move)

import monte_carlo_testsuite2 as wopr
wopr.test_mc_move(mc_move)
