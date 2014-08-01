"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui

DIRECTIONS = {"u" : -1,
              "d" : 1,
              "r" : 1,
              "l" : -1}

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """

        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans


    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def _get_grid(self):
        """
        Return a copy of the game grid.
        """
        return list(self._grid)

    def _get_solved_grid(self):
        """
        Helper method returs the grid as it would be if it were
        solved.
        """
        idx = 0
        solved = [ [row + col for col in range(self.get_width())] for row in range(self.get_height())]
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                solved[row][col] = idx
                idx += 1 
        return solved

    def _get_right_of_zero(self, grid, target_row, target_col):
        """
        Helper method gets the values of the tiles to the right of zero.
        """
        return grid[target_row][target_col + 1:self.get_width()]


    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        current_grid = self._get_grid()
        solved_grid = self._get_solved_grid()
        
        # If zero ends up in the target position and the current 
        # bottom row is solved and the tiles to the right of 
        # the target (zero) are solved.
        if  self.get_number(target_row, target_col) == 0 and \
            current_grid[self.get_height() - 1] == solved_grid[self.get_height() - 1] and \
            self._get_right_of_zero(current_grid, target_row, target_col) == self._get_right_of_zero(solved_grid, target_row, target_col):
            return True
        # If the target_row is the bottom row and 0 is in the 
        # target position and all tiles to the right of zero are solved.
        elif target_row == self.get_height() -1 and \
            self.get_number(target_row, target_col) == 0 and \
            self._get_right_of_zero(current_grid, target_row, target_col) == self._get_right_of_zero(solved_grid, target_row, target_col):
            return True
        # If zero ends up in the target position and it's also 
        # in the bottom right corner.
        elif self.get_number(target_row, target_col) == 0 and  self.get_number(self.get_height() -1, self.get_width() - 1) == 0:
            return True
        else:
            return False

    def _is_legal(self, direction, row, col):
        """
        Helper method calculates if a given move is legal.
        Returns boolean.
        """
        zero_row, zero_col = self.current_position(row, col)

        if direction == "u" and zero_row < 0:
            return False
        elif direction == "d" and zero_row + DIRECTIONS[direction] < self._height - 1:
            return False
        elif direction == "l" and zero_col < 0:
            return False
        elif direction == "r" and zero_col > self._width - 1:
            return False
        else:
            return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # Moves that satisfy the lower_row_invariant
        move_string = "lddruld"

        # Moves that stay within the grid.
        actual_move = ""

        for move in move_string:
            if self._is_legal(move, target_row, target_col):
                self.update_puzzle(move)
        return ""

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))



