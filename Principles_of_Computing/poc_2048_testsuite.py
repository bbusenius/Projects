"""
A simple testing suite for Solitaire Mancala
Note that tests are not exhaustive and should be supplemented
"""

import poc_simpletest

# Test the helper function
def run_merge_test(merge):
    """
    Unit test the merge function 
    """
    
    # Create a TestSuite object
    suite = poc_simpletest.TestSuite()   
 
    # Test the merge function
    suite.run_test(merge([2, 0, 2, 2]), [4, 2, 0, 0], "merge 1:")
    suite.run_test(merge([2, 0, 2, 4]), [4, 4, 0, 0], "merge 2:")
    suite.run_test(merge([0, 0, 2, 2]), [4, 0, 0, 0], "merge 3:")
    suite.run_test(merge([2, 2, 0, 0]), [4, 0, 0, 0], "merge 4:")
    suite.run_test(merge([2, 2, 2, 2]), [4, 4, 0, 0], "merge 5:")
    suite.run_test(merge([8, 16, 16, 8]), [8, 32, 8, 0], "merge 6:")


# Unit testing for the game class
def run_test(game_class):
    """
    Some informal testing code
    """
    
    # Create a TestSuite object
    suite = poc_simpletest.TestSuite()

    # Create a game
    game = game_class(6, 6)
    
    # Test is_game_won
    suite.run_test(game.test(), "foobar", "test")                     

    # Report number of tests and failures
    suite.report_results()

