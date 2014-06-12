"""
Clone of 2048 game.
"""

#import poc_2048_gui        

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)}
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    results = [0] * len(line)
    index = 0
    for tile in line:
        if tile != 0:
            
            if tile == results[index - 1]:
                results[index - 1] = tile * 2
                merged = True
            else:
                merged = False
                results[index] = tile
            # Only advance the counter if it's not a 0
            index += 1
           
    for number in range(len(results)):
        if results[number] == 0:
            results.pop(number)
            results.append(0)

    return results

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        pass

    def test(self):
        return "foobar"
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        # replace with your code
        pass
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        pass

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return 0
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return 0
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        pass
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        pass
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        # replace with your code
        pass

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return 0
 
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
import poc_2048_testsuite
poc_2048_testsuite.run_merge_test(merge)
poc_2048_testsuite.run_test(TwentyFortyEight)
