"""
Clone of 2048 game.
"""

#import poc_2048_gui        
import random

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
    Helper function that merges a single row or column in 2048.
    """
    # Blank results list matching the length of the line
    results = [0] * len(line)
    index = 0
    # Loop over the line and put numbers that aren't 0 together in the results
    for tile in line:
        if tile != 0:
            results[index] = tile
            # Only advance the counter if it's not a 0
            index += 1
    # Loop over the results and merge numbers
    for number in range(len(results)):
        if number > 0 and results[number] == results[number - 1]:
            results[number - 1] = results[number] * 2
            results.append(0)
            results.pop(number)
   
    return results

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """Initialize the object."""
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = ''

        # Create a dictionary of indicies for tiles in rows representing 
        # the directions UP, DOWN, LEFT, and RIGHT. These are the uppermost,
        # leftmost, rightmost and downmost coordinates on the grid.
        self._up_index = {UP : []}
        self._left_index = {LEFT : []}
        self._right_index = {RIGHT : []}
        self._down_index = {DOWN : []}

        # Loop over the width and height of the grid and build the dictionaries
        # of directional coordinates above.
        for height_matrix in range(self._grid_height):
            for width_matrix in range(self._grid_width):
                if height_matrix == 0:
                    self._up_index[UP].append((height_matrix, width_matrix))
                if width_matrix < 1:
                    self._left_index[LEFT].append((height_matrix, width_matrix))
                if width_matrix == self._grid_width - 1:
                    self._right_index[RIGHT].append((height_matrix, width_matrix))
                if height_matrix == self._grid_height - 1:
                    self._down_index[DOWN].append((height_matrix, width_matrix))

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        cells = [ [0 for col in range(self.get_grid_width())] for row in range(self.get_grid_height())]
        self._grid = cells
        return cells
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ''
        for row in self._grid:
            string += str(row) + '\n'
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        pass

    def get_empty_tiles(self):
        """
        Get a list of tuples representing all of the 
        empty tiles that contain zeros.
        """
        empty_squares = []
        row_num = 0
        for row in self._grid:
            column_num = 0 
            for column in row:
                if column == 0:
                    empty_squares.append((row_num, column_num))
                column_num += 1 
            row_num += 1
        return empty_squares
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_tiles = self.get_empty_tiles() 
        random_empty_tile = random.choice(empty_tiles)
        value = random.choice([2] * 9 + [4])
        self.set_tile(random_empty_tile[0], random_empty_tile[1], value)
                
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """ 
        self._grid[row][col] = value     

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self._grid[row][col]
 
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
import poc_2048_testsuite
poc_2048_testsuite.run_merge_test(merge)
poc_2048_testsuite.run_test(TwentyFortyEight)
