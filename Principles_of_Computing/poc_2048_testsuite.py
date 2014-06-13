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

    # Test 1
    game1 = game_class(4, 4)
    game1.reset()
    game1.set_tile(1, 1, 4)
    game1.new_tile()
    print(game1)
    suite.run_test(game1.get_tile(1, 1), 4, "Test game1 get_tile()")
    suite.run_test(game1.get_tile(2, 3), 0, "Test game1 get_tile()")
    suite.run_test(game1.reset(), [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], "Test game1 reset()")   

    # Test 2
    game2 = game_class(3, 3)
    game2.reset()
    game2.set_tile(2, 2, 7)
    print(game2)
    suite.run_test(game2.get_tile(2, 2), 7, "Test game2 get_tile()")
    suite.run_test(game2.get_tile(1, 1), 0, "Test game2 get_tile()") 
    suite.run_test(game2.reset(), [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "Test game2 reset()") 

    # Test 3
    game3 = game_class(2, 7)
    game3.reset()
    game3.set_tile(0, 4, 3)
    print(game3)
    suite.run_test(game3.get_tile(0, 4), 3, "Test game3 get_tile()")
    suite.run_test(game3.get_tile(1, 6), 0, "Test game3 get_tile()") 
    suite.run_test(game3.reset(), [[0, 0, 0, 0, 0, 0, 0 ], [0, 0, 0, 0, 0, 0, 0]], "Test game3 reset()")  

    # Test 4: Test new_tile method 
    game4 = game_class(3, 3)
    game4.reset()
    game4.set_tile(0, 0, 8)
    game4.set_tile(0, 1, 8)
    game4.set_tile(0, 2, 8)
    game4.set_tile(1, 0, 8)
    game4.set_tile(1, 1, 8)
    game4.set_tile(1, 2, 8)
    game4.new_tile()
    print(game4)
    #suite.run_test(game4.get_tile(2, 2), 7, "Test game4 get_tile()")
    #suite.run_test(game4.get_tile(1, 1), 0, "Test game4 get_tile()") 
    #suite.run_test(game4.reset(), [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "Test game4 reset()")  

    # Report number of tests and failures
    suite.report_results()

