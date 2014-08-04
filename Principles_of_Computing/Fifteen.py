"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui

DIRECTIONS = {"u" : (-1, 0),
              "d" : (1, 0),
              "r" : (0, 1),
              "l" : (0, -1)}

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

    def _get_tile_pos(self, num):
        """
        Helper method returns the current position of zero.

        Args:
            num: integer, the tile value who's position we want.

        Returns:
            Tuple, row and column containing the value of zero.
        
        """
        row_count = 0
        num_pos = None
        for row in self._get_grid():
            if num in row:
                num_pos = (row_count, row.index(num))
                break;
            row_count += 1
        return num_pos
        

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

    def _is_legal(self, move, target_row, target_col):
        """
        Helper method calculates if a given move is legal.
        Returns boolean.
        """
        if move == "u" and target_row + DIRECTIONS[move] < 0:
            return False
        elif move == "d" and target_row + DIRECTIONS[move] < self._height - 1:
            return False
        elif move == "l" and target_col + DIRECTIONS[move] < 0:
            return False
        elif move == "r" and target_col + DIRECTIONS[move] > self._width - 1:
            return False
        else:
            return True

    def _in_position(self, target_pos, current_pos, solve_col = False):
        """
        Helper function checks if the zero tile and the 
        target tile are both in the correct final position.
    
        Args:
            target_pos: tuple, the target final position.

            current_pos: tuple, the current position.

        Returns:
            boolean
        """
        return current_pos == target_pos and ((self._get_tile_pos(0) == (target_pos[0], target_pos[1] - 1) or (solve_col == True)) )


    def _apply_cycle(self, cycle, target, final_target_pos, solve_col = False):
        """
        Applies cyclical moves and updates the puzzle as needed.
        
        Returns:
            string, moves needed for completion.
        """
        moves = ""
        # Repeat the cycle until the tile is in position.
        # Always put the zero to the left of the target tile in the end.
        #print not self._in_position(final_target_pos, self._get_tile_pos(target), solve_col)
        while not self._in_position(final_target_pos, self._get_tile_pos(target), solve_col):
            # Move the target down using cyclical moves
            for move in cycle:
                # Terminate if we're in the proper position
                if self._in_position(final_target_pos, self._get_tile_pos(target), solve_col):
                    break       
                
                # Append and move
                moves += move
                self.update_puzzle(move)
        
        return moves

    def _move_to_target(self, current_target_pos, zero_pos):
        """
        Moves the zero tile to the target.
        """
        moves = ""
        # Move zero to the target tile
        while current_target_pos[0] < zero_pos[0]:
            moves += "u"
            self.update_puzzle("u")
            zero_pos = self._get_tile_pos(0)
        while current_target_pos[1] < zero_pos[1]:
            moves += "l"
            self.update_puzzle("l")
            zero_pos = self._get_tile_pos(0)
        while current_target_pos[1] > zero_pos[1]:
            moves += "r"
            self.update_puzzle("r")
            zero_pos = self._get_tile_pos(0)
        
        return moves


    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # Convenience variables
        
        # The target we wish to move
        target = self._get_solved_grid()[target_row][target_col]
        # The initial position of 0
        zero_pos = self._get_tile_pos(0)
        # The initial position of the target we wish to move
        target_pos = self._get_tile_pos(target)
        #The final position of the target
        final_target_pos = (target_row, target_col)
        # The halfway point where upward moves branch left or right
        memory_point = (target_pos[0], target_col)

        #print "CRGRID", self._get_grid()
        #print "TARGET", target
        #print "ZEROPO", zero_pos
        #print "TARGPO", target_pos
        #print "FINAL", final_target_pos

        # Moves that stay within the grid.
        all_moves = ""
 
        # Target is in the same column as zero  
        if target_pos[0] < final_target_pos[0] and target_pos[1] == final_target_pos[1]:

            # Move to target
            all_moves += self._move_to_target(target_pos, zero_pos)

            # Cycle the tile to the memory point (y axis)
            all_moves += self._apply_cycle("lddrl", target, final_target_pos)

       
        # Target is in the same row as zero
        elif target_pos[1] < zero_pos[1] and target_pos[0] == zero_pos[0]:

            # Move to target
            all_moves += self._move_to_target(target_pos, zero_pos)

            # Cycle the tile to the memory point (y axis)
            all_moves += self._apply_cycle("urrdl", target, final_target_pos)

        # Target is above and to the LEFT of zero
        elif target_pos[0] < zero_pos[0] and target_pos[1] < zero_pos[1]:
            # Move to target
            all_moves += self._move_to_target(target_pos, zero_pos)
            # Cycle the tile to the memory point (y axis)
            all_moves += self._apply_cycle("drrul", target, memory_point)
            # Cycle the tile down to it's final position
            # Target is in top row
            if target_pos[0] == 0:
                all_moves += self._apply_cycle("drul", target, (memory_point[0] + 1, memory_point[1]))
            all_moves += self._apply_cycle("druld", target, final_target_pos)

        # Target is above and to the RIGHT of zero
        elif target_pos[0] < zero_pos[0] and target_pos[1] > zero_pos[1]:
            # Move to target
            all_moves += self._move_to_target(target_pos, zero_pos)
            # Cycle the tile to the memory point (y axis)
            all_moves += self._apply_cycle("ulldr", target, memory_point)
            # Cycle the tile down to it's final position
            all_moves += self._apply_cycle("druld", target, final_target_pos)

        return all_moves

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # The target we wish to move
        target = self._get_solved_grid()[target_row][0]
        # The initial position of 0
        zero_pos = self._get_tile_pos(0)
        # The initial position of the target we wish to move
        target_pos = self._get_tile_pos(target)
        #The final position of the target
        final_target_pos = (target_row, 0)

        # Moves that stay within the grid.
        all_moves = ""
        
        # Move up and to the right first, for all cases
        all_moves += "ur"
        self.update_puzzle("ur")
    
        # If the target is already in position
        # move to he end of the line. In this case
        # the "target" is not the final destination 
        # but rather the end of the row.
        if self._get_tile_pos(target) == final_target_pos:
            #return "rr"
            if self.get_width() > 2:
                all_moves += self._move_to_target((target_row - 1, self.get_width() - 1), (target_row - 1, 1))

        # Otherwise reposition the target tile to 
        # position (i-1,1) and the zero tile to position (i-1,0)
        else:
            # Move to the target
            all_moves += self._move_to_target(target_pos, self._get_tile_pos(0))

            # Solve for corner case (top row, right corner)
            if target_pos[0] == 0 and target_pos[1] == self.get_width() - 1:
                all_moves += "dluld"
                self.update_puzzle("dluld")
            # Solve for case when target tile is one column over and on the top row
            elif target_pos == (0, 1):
                all_moves += "ld"
                self.update_puzzle("ld")
            # Solve for corner case (top row left corder)
            elif target_pos == (0, 0):
                all_moves += "druld"
                self.update_puzzle("druld")
            # Target is not in the top row
            elif target_pos[0] != 0:
                # Cycle the tile to the memory point (y axis) -> WATCH THE MAGIC # 1 
                all_moves += self._apply_cycle("ulldr", target, (target_pos[0], 1), False)
                
            # Solve for normal cases in the top row
            #elif target_pos[0] == 0:
            #    all_moves += "dlul"
            #    self.update_puzzle("dlul")
            
            # Cycle for solving the column
            all_moves += self._apply_cycle("ruldrdlurdluurddlu", target, final_target_pos, True)

            # Move to the end of the row
            all_moves += self._move_to_target((self._get_tile_pos(target)[0], self.get_width() - 1), zero_pos)

        if all_moves == "urr":
            self.update_puzzle("urr")
            return "urr"

        return all_moves

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



