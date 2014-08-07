import poc_simpletest
from Fifteen import Puzzle

def test_phase1():
    """
    Testing code to debug phase1 for 15puzzle
    """

    suite = poc_simpletest.TestSuite()
        
    #############################
    ### lower_row_invariant TESTS
    
    puzzle = Puzzle(3, 3, [[2, 3, 4], [1, 0, 5], [6, 7, 8]])
    suite.run_test(puzzle.lower_row_invariant(1, 1), True, "Test A1:")
    
    puzzle = Puzzle(3, 3, [[2, 3, 4], [5, 0, 1], [6, 7, 8]])
    suite.run_test(puzzle.lower_row_invariant(1, 1), False, "Test A2:")
    
    puzzle = Puzzle(4, 4, [[1, 2, 3, 4], [5, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.lower_row_invariant(1, 1), True, "Test A3:")
    
    puzzle = Puzzle(4, 4, [[1, 2, 3, 7], [5, 0, 6, 4], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.lower_row_invariant(1, 1), False, "Test A4:")
    
    puzzle = Puzzle(3, 5, [[1, 2, 3, 4, 5], [6, 7, 0, 8, 9], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.lower_row_invariant(1, 2), True, "Test A5:")
    
    puzzle = Puzzle(3, 5, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 0], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.lower_row_invariant(1, 4), True, "Test A6:")
    
    puzzle = Puzzle(3, 5, [[13, 1, 2, 3, 11], [5, 6, 7, 8, 10], [11, 12, 4, 0, 14]])
    suite.run_test(puzzle.lower_row_invariant(2, 3), True, "Test A7:")
    
    #############################
    ### solve_interior_tile TESTS 
    
    puzzle = Puzzle(3, 3, [[1, 2, 3], [4, 5, 7], [6, 0, 8]])
    suite.run_test(puzzle.solve_interior_tile(2, 1), "urullddruld", "Test B1:")
    
    puzzle = Puzzle(3, 3, [[1, 2, 3], [4, 5, 6], [7, 0, 8]])
    suite.run_test(puzzle.solve_interior_tile(2, 1), "l", "Test B2:")

    ##puzzle = Puzzle(4, 4, [[5, 4, 1, 3], [8, 0, 2, 7], [10, 13, 6, 11], [9, 12, 14, 15]])
    ##suite.run_test(puzzle.solve_interior_tile(1, 1), "lddruld", "Test Homework solve_interior_tile:")
    
    puzzle = Puzzle(4, 4, [[1, 2, 3, 4], [5, 6, 10, 7], [8, 9, 0, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.solve_interior_tile(2, 2), "uld", "Test B3:")
    
    puzzle = Puzzle(4, 4, [[1, 2, 3, 4], [5, 6, 7, 9], [8, 0, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.solve_interior_tile(2, 1), "urrulldrullddruld", "Test B4:")

    puzzle = Puzzle(3, 5, [[13, 2, 3, 4, 5], [6, 7, 8, 9, 11], [10, 12, 1, 0, 14]])
    suite.run_test(puzzle.solve_interior_tile(2, 3), "uullldrruldrruldrulddruld", "Test B5:")
                                            
    #############################
    ### solve_col0_tile TESTS   

    puzzle = Puzzle(1, 1, [[0]])
    suite.run_test(puzzle.solve_col0_tile(0), "", "Test 1x1 grid:")

    # Test 2x3 grid problems with already positioned tile
    puzzle = Puzzle(3, 2, [[1, 2],[4, 3],[0, 5]])
    suite.run_test(puzzle.solve_col0_tile(2), "ur", "Test 2x3 grid: tile placed correctly after first move.")

    # Test Upper right corner on a large grid
    puzzle = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
    suite.run_test(puzzle.solve_col0_tile(3), "uruurrrdllurdllurdlulddrulddruldrrrr", "Test C1:")

    #puzzle = Puzzle(4, 5, [[8, 2, 10, 9, 1], [7, 6, 5, 4, 3], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
    #suite.run_test(puzzle.solve_col0_tile(2), "I don't remember what I'm testing", "Test C1:")

    puzzle = Puzzle(3, 3, [[1, 2, 3], [6, 4, 5], [0, 7, 8]])
    suite.run_test(puzzle.solve_col0_tile(2), "urr", "Test C1:")
    
    puzzle = Puzzle(3, 3, [[2, 3, 6], [1, 4, 5], [0, 7, 8]])
    suite.run_test(puzzle.solve_col0_tile(2), "ururdluldruldrdlurdluurddlurr", "Test C2:")

    puzzle = Puzzle(3, 3, [[2, 6, 1], [3, 4, 5], [0, 7, 8]])
    suite.run_test(puzzle.solve_col0_tile(2), "uruldruldrdlurdluurddlurr", "Test C3:")

    puzzle = Puzzle(3, 3, [[6, 2, 1], [3, 4, 5], [0, 7, 8]])
    suite.run_test(puzzle.solve_col0_tile(2), "uruldruldruldrdlurdluurddlurr", "Test C4:")

    puzzle= Puzzle(3, 5, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [0, 11, 12, 13, 14]])
    suite.run_test(puzzle.solve_col0_tile(2), "urrrrulldrulldrulldruldrdlurdluurddlurrrr", "Test C5:")
                                                       
    puzzle = Puzzle(3, 5, [[10, 2, 3, 4, 5], [6, 7, 8, 9, 1], [0, 11, 12, 13, 14]])
    suite.run_test(puzzle.solve_col0_tile(2), "uruldruldruldrdlurdluurddlurrrr", "Test C6:")
    
    puzzle = Puzzle(3, 5, [[1, 2, 10, 4, 5], [6, 7, 8, 9, 3], [0, 11, 12, 13, 14]])
    suite.run_test(puzzle.solve_col0_tile(2), "ururdluldruldrdlurdluurddlurrrr", "Test C7:")
    
    # get testing results
    return suite.report_results()

def test_phase2():
    
    suite = poc_simpletest.TestSuite()

    #############################
    ### row1_invariant TESTS       
    
    puzzle = Puzzle(3, 3, [[2, 3, 4], [1, 0, 5], [6, 7, 8]])
    suite.run_test(puzzle.row1_invariant(1), False, "Test A1:")
    
    puzzle = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
    suite.run_test(puzzle.row1_invariant(1), True, "Test A2:")
    
    puzzle = Puzzle(3, 3, [[2, 3, 4], [5, 1, 0], [6, 7, 8]])
    suite.run_test(puzzle.row1_invariant(2), True, "Test A3:")
 
    puzzle = Puzzle(4, 4, [[1, 3, 4, 2], [0, 6, 5, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.row1_invariant(0), False, "Test A4:")
    
    puzzle = Puzzle(3, 5, [[1, 2, 3, 4, 5], [8, 9, 0, 6, 7], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.row1_invariant(2), False, "Test A5:")
    
    puzzle = Puzzle(3, 5, [[1, 5, 2, 3, 4], [7, 6, 0, 8, 9], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.row1_invariant(2), True, "Test A6:")
    
    puzzle = Puzzle(3, 5, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 0], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.row1_invariant(4), True, "Test A7:")
    
    #############################
    ### row0_invariant TESTS       
    
    puzzle = Puzzle(3, 3, [[2, 0, 1], [3, 4, 5], [6, 7, 8]])
    suite.run_test(puzzle.row0_invariant(1), False, "Test B1:")
    
    puzzle = Puzzle(3, 3, [[1, 0, 2], [3, 4, 5], [6, 7, 8]])
    suite.run_test(puzzle.row0_invariant(1), True, "Test B2:")
    
    puzzle = Puzzle(4, 4, [[1, 0, 3, 2], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.row0_invariant(1), False, "Test B3:")

    puzzle = Puzzle(4, 4, [[1, 0, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.row0_invariant(1), True, "Test B4:")
    
    puzzle = Puzzle(3, 5, [[1, 2, 3, 4, 0], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.row0_invariant(4), True, "Test B5:")
    
    puzzle = Puzzle(3, 5, [[2, 4, 1, 0, 3], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.row0_invariant(3), False, "Test B6:")
    
    #############################
    ### solve_row1_tile TESTS     
    
    puzzle = Puzzle(3, 3, [[1, 4, 2], [3, 5, 0], [6, 7, 8]])
    suite.run_test(puzzle.solve_row1_tile(2), "lur", "Test C1:")
 
    puzzle = Puzzle(4, 4, [[1, 2, 6, 3], [7, 4, 5, 0], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.solve_row1_tile(3), "lllurrdlurrdlur", "Test C2:")

    puzzle = Puzzle(4, 4, [[1, 7, 4, 2], [3, 5, 6, 0], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.solve_row1_tile(3), "ulldrruldru", "Test C3:")
                                               
    puzzle = Puzzle(3, 5, [[1, 2, 7, 3, 4], [6, 5, 0, 8, 9], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.solve_row1_tile(2), "u", "Test C4:")
    
    puzzle = Puzzle(3, 5, [[1, 7, 2, 3, 4], [6, 5, 0, 8, 9], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.solve_row1_tile(2), "uldru", "Test C5:")
    
    puzzle = Puzzle(3, 5, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 0], [10, 11, 12, 13, 14]])
    suite.run_test(puzzle.solve_row1_tile(4), "lur", "Test C6:")
    
    #############################
    ### solve_row0_tile TESTS  
    
    puzzle = Puzzle(3, 3, [[1, 2, 0], [3, 4, 5], [6, 7, 8]])
    suite.run_test(puzzle.solve_row0_tile(2), "ld", "Test D1:")
 
    puzzle = Puzzle(4, 4, [[2, 4, 5, 0], [3, 6, 1, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.solve_row0_tile(3), "ldllurrdlurdlurrdluldrruld", "Test D2:")

    puzzle = Puzzle(4, 4, [[1, 3, 5, 0], [2, 6, 4, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    suite.run_test(puzzle.solve_row0_tile(3), "lduldruldurdlurrdluldrruld", "Test D3:")

    puzzle = Puzzle(4, 5, [[1, 5, 6, 0, 4], [7, 2, 3, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
    suite.run_test(puzzle.solve_row0_tile(3), "lduldurdlurrdluldrruld", "Test D4:")
    
    # get testing results
    return suite.report_results()
    
def test_phase3():
    
    suite = poc_simpletest.TestSuite()

    #############################
    ### solve_2x2 TESTS 
    
    puzzle = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
    suite.run_test(puzzle.solve_2x2(), "uldrul", "Test A1:")
    
    #puzzle = Puzzle(3, 5, [[5, 1, 2, 3, 4], [6, 0, 7, 8, 9], [10, 11, 12, 13, 14]])
    #suite.run_test(puzzle.solve_2x2(), "ulrdlu", "Test A2:")

    puzzle = Puzzle(2, 2, [[3, 2], [1, 0]])
    suite.run_test(puzzle.solve_2x2(), "uldrul", "Test A3:")

    puzzle = Puzzle(2, 2, [[1, 3], [2, 0]])
    suite.run_test(puzzle.solve_2x2(), "ul", "Test A4:")

    #############################
    ### solve_puzzle TESTS     
    
    #puzzle = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
    #suite.run_test(puzzle.solve_puzzle(), "lddduuurdlulddrulddrulduruulddruldruldrdlurdluurddlurrrrllluuldrulddrulduruldruldrdlurdluurddlurrrrlurldlurlduldul", "Test B1:")
    
    return suite.report_results()

#test_phase1()
#test_phase2()
test_phase3()
