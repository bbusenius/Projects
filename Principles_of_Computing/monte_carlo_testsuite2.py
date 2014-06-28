"""
Test suite for Tic-Tac-Toe (Monte Carlo)

Author: Jason Youzwak
"""

import poc_simpletest
import poc_ttt_provided as provided
import math

# Dimension of the Tic Tac Toe Grid
DIM = 3

def get_num_squares(board, player):
    """
    Determine the number of squares occupied by a player
    """
    num_squares = 0
    dim = board.get_dim()
    for row in range(dim):
        for col in range(dim):
            if board.square(row, col) == player:
                num_squares += 1
    return num_squares
                
def test_mc_trial(mc_trial):
    """
    Test the mc_trial method:
    1) The trial ends with a win or a draw
    2) The trial does not modify already occupied spaces 
    3) The trial alternates players properly
    """

    # Create a test suite
    suite0 = poc_simpletest.TestSuite()
    
    # Create a 3x3 board
    board = provided.TTTBoard(3)
            
    # Run a single trial
    mc_trial(board, provided.PLAYERX)

    # Check that the trial ends with the game won or a draw
    suite0.run_test(board.check_win() != None, True, "Test 1: mc_trial ends with winner or draw: ")

    # Create another 3x3 board
    board = provided.TTTBoard(3)
    
    # Place some squares on the board
    board.move(0, 0, provided.PLAYERX)
    board.move(0, 1, provided.PLAYERO)
    board.move(0, 2, provided.PLAYERX)
    
    # Display the initial board
    print "Initial Board: \n", board
    
    # Run a single trial
    mc_trial(board, provided.PLAYERO)

    # Display the board after the trial
    print "Board after Monte Carlo trial: \n", board

    # Check that the spaces that were already occupied were not modified by the trial     
    suite0.run_test(board.square(0,0), provided.PLAYERX, "Test 2A: mc_trial did not modify existing pieces: ")
    suite0.run_test(board.square(0,1), provided.PLAYERO, "Test 2B: mc_trial did not modify existing pieces: ")
    suite0.run_test(board.square(0,2), provided.PLAYERX, "Test 2C: mc_trial did not modify existing pieces: ")

    # Get the number of squares occupied by each player
    num_xs = get_num_squares(board, provided.PLAYERX)
    num_os = get_num_squares(board, provided.PLAYERO)
    
    # Check that the trial switched players properly
    suite0.run_test(math.fabs(num_xs - num_os) <= 1, True, "Test 3: mc_trial altered player turns: ")
         
    suite0.report_results()

def initial_board():
    """
    Create a Tic Tac Toe game in progress:
    X |   | 
   ------------
      | X | O
   ------------
      |   | O
    """
    # Create a 3x3 board
    board = provided.TTTBoard(DIM)

    # Place some pieces on the board 
    board.move(0, 0, provided.PLAYERX)
    #board.move(0, 1, provided.EMPTY)
    #board.move(0, 2, provided.EMPTY)
    
    #board.move(1, 0, provided.EMPTY)
    board.move(1, 1, provided.PLAYERX)
    board.move(1, 2, provided.PLAYERO)

    #board.move(2, 0, provided.PLAYERO)
    #board.move(2, 1, provided.EMPTY)
    board.move(2, 2, provided.PLAYERO)
    
    return board
    
def board_player_x_wins():
    """
    Continue the game by moving X to a winning spot
    X | O | X
   ------------
      | X | O
   ------------
    X |   | O
    """
    # Create the initial board
    board = initial_board()

    # Place some pieces on the board 
    board.move(0, 2, provided.PLAYERX)
    board.move(0, 1, provided.PLAYERO)
    board.move(2, 0, provided.PLAYERX)
    
    return board

def board_player_o_wins():
    """
    Continue the game by moving O to a winning spot
    X | X | O
   ------------
      | X | O
   ------------
      |   | O
    """
    # Create the initial board
    board = initial_board()

    # Place some pieces on the board 
    board.move(0, 1, provided.PLAYERX)
    board.move(0, 2, provided.PLAYERO)
    
    return board

def board_tied_game():
    """
    Create a Tic Tac Toe game in progress:
    X | O | X
   ------------
    X | X | O
   ------------
    O | X | O
    """

    # Create the initial board
    board = initial_board()

    # Place some pieces on the board 
    board.move(0, 2, provided.PLAYERX)
    board.move(2, 0, provided.PLAYERO)
    board.move(2, 1, provided.PLAYERX)
    board.move(0, 1, provided.PLAYERO)
    board.move(1, 0, provided.PLAYERX)
    
    return board

def create_empty_scores():
    """
    Create a DIMxDIM array of empty scores
    """
    return [[0 for dummycol in range(DIM)] 
                           for dummyrow in range(DIM)]

def test_mc_update_scores(mc_update_scores):
    """
    Test the mc_update_scores method:
    3) Score of a square in a tie game is zero
    4) Score of an X square in a player X won game is positive  
    5) Score of an O square in a player X won game is negative 
    6) Score of an X square in a player O won game is negative
    7) Score of an O square in a player O won game is positive 
    """
    
    # Create a test suite
    suite1 = poc_simpletest.TestSuite()
    
    # Initialize the scores to empty    
    scores = create_empty_scores()
    
    tied_board = board_tied_game()
    mc_update_scores(scores, tied_board, provided.PLAYERX)

    suite1.run_test(scores[0][0], 0, "Test 3: test_mc_update_scores reports tie game")

    # Initialize the scores to empty    
    scores = create_empty_scores()
    
    player_x_wins = board_player_x_wins()
    mc_update_scores(scores, player_x_wins, provided.PLAYERX)
    
    suite1.run_test(scores[0][0] > 0, True, "Test 4: test_mc_update_scores reports player x wins")
    suite1.run_test(scores[0][1] < 0, True, "Test 5: test_mc_update_scores reports player x wins")

    # Reset scores to empty    
    scores = create_empty_scores()

    player_o_wins = board_player_o_wins()
    mc_update_scores(scores, player_o_wins, provided.PLAYERX)

    suite1.run_test(scores[0][0] < 0, True, "Test 6: test_mc_update_scores reports player o wins")
    suite1.run_test(scores[0][2] > 0, True, "Test 7: test_mc_update_scores reports player o wins")

    suite1.report_results()

def test_get_best_move(get_best_move):
    """
    Test the get_best_move method:
    8) The highest value score is chosen
    9) Only scores from empty squares are considered
    10) The highest value score is chosen randomly
    """
    
    # Create a test suite
    suite2 = poc_simpletest.TestSuite()
    
    # Initialize the scores to empty    
    scores = create_empty_scores()

    # Create a board with pieces already placed    
    board = initial_board()
    
    # Test X winning space
    scores = [[0.0, -2.0, 2.0], [0, 0.0, 0.0], [1.0, 0, 0.0]]
    suite2.run_test(get_best_move(board, scores), (0,2), "Test 8: get_best_move returns highest value")

    # Test X winning space, when other non-empty spaces have higher score
    scores = [[10.0, -2.0, 2.0], [0, 5.0, 0.0], [1.0, 0, 0.0]]
    suite2.run_test(get_best_move(board, scores), (0,2), "Test 9: get_best_move choses empty spaces from the board")

    # Test X winning space, when other non-empty spaces have higher score
    scores = [[1.0, -1.0, 1.0], [1.0, 7.0, 7.0], [9.0, 9.0, 1.0]]

    # Test win there are multiple high scores
    moves = set()
    for i in range(50):
        move = get_best_move(board, scores)
        moves.add(move)
    expected = set()
    expected.add((2,0))
    expected.add((2,1))
    
    suite2.run_test(moves, expected, "Test 10: get_best_move choses random value from matched pairs")

    suite2.report_results()

def test_mc_move(mc_move):
    """
    Test the mc_move method:
    11) Best move is chosen for Player X
    12) Best move is chosen for Player O
    """
    # Create a test suite
    suite3 = poc_simpletest.TestSuite()

    # Create a board with pieces already placed    
    board = initial_board()

    # Run the tests
    suite3.run_test(mc_move(board, provided.PLAYERX, 100), (0,2), "Test 11: mc_move chose the best move for player x")
    suite3.run_test(mc_move(board, provided.PLAYERO, 100), (0,2), "Test 12: mc_move chose the best move for player o")

    suite3.report_results()

