"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
#import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = [] 
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
    

    def __str__(self):
        """
        String representation of the game state.
        H = human, Z = zombie, O = obstacle, E = zombie eating human
        """
        z_distance = self.compute_distance_field(HUMAN)
        cells = [ [ str(z_distance[row][col]) for col in range(self._grid_width)] for row in range(self._grid_height)] 
        for row, col in self.__get_human_list():
            cells[row][col] = "H"
        for row, col in self.__get_zombie_list():
            if (row, col) in self.__get_human_list():
                cells[row][col] = "E"
            else:
                cells[row][col] = "Z"
        for row, col in self.__get_obstacle_list():
            cells[row][col] = "_" 

        string = str(cells) 
        string = string.replace("[[", " [")
        string = string.replace("]]", "]")
        string = string.replace("],", "]\n")
          
        return string 
 
    def __get_obstacle_list(self):
        """
        Return a list of obstacles.
        """
        return self._obstacle_list

    def __get_human_list(self):
        """
        Return a list of humans.
        """
        return self._human_list

    def __get_zombie_list(self):
        """
        Return a list of zombies.
        """
        return self._zombie_list 

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
 
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)  
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return (human for human in self._human_list)

    def get_entity_list(self, entity_type):
        """
        Return a list of entities (humans or zombies).

        Args:
            entity_type, string "zombie", "human", or "obstacle".
       
        Returns:    
            A list **copy** of self._human_list or self._zombie_list.
        """
        # A dictionary of humans or zombies to add to the queue.
        entity_lists = { HUMAN  : list(self.__get_human_list()),
                         ZOMBIE : list(self.__get_zombie_list()) }

        return entity_lists[entity_type.lower()]
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
    
        Args:
            entity_type, string "zombie", "human", or "obstacle".
        """
        # Initialize a grid the same size as our other.
        # The terminology used in the instructions for this was absolutely terrible
        # so be careful with this. If there are future problems look here.
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
       
        # Set all of the cells in visited to empty. Maybe a little paranoid... 
        # They start out as empty but we're going to do it anyhow just in case. 
        visited.clear()

        # Setup distance_field as a list. Again the instructions for this were 
        # absolutely terrible so watchout here. 
        distance_field = [[ self.get_grid_width() * self.get_grid_height() for dummy_col in range(self.get_grid_width())] for dummy_row in range(self.get_grid_height())] 

        # Create an empty queue for tracking humans or zombies.
        boundary = poc_queue.Queue()

        # Add humans or zombies to the queue and initialize 
        # the proper values in visited and distance_field
        for item in self.get_entity_list(entity_type):
            boundary.enqueue(item)
            # Mark the grid square as FULL
            visited.set_full(item[0], item[1])
            # Set distance_field cells in boundary queue to 0
            distance_field[item[0]][item[1]] = 0

        ### End initialization ###
       
        # Use a breadth-first search to compute 
        # the distance between humans and zombies.
        while len(boundary) > 0:
            neighbor_cells = []
            current_cell = boundary.dequeue()
            neighbor_cells.extend(self.four_neighbors(current_cell[0], current_cell[1]))
            # Distance is the position of the current cell + 1 (incrementing is not necessary)
            distance = distance_field[current_cell[0]][current_cell[1]] + 1
            for row, col in neighbor_cells:
                # If there isn't an obstacle
                # if self.is_empty(row, col):
                if (row, col) not in self.__get_obstacle_list():
                    # If the cell hasn't been visited
                    if visited.is_empty(row, col) :
                        visited.set_full(row, col)
                        distance_field[row][col] = distance
                        boundary.enqueue((row, col))
        return distance_field 

    
    def __get_move(self, distances, entity, current_cell):
        """
        Method gets possible routs for zombies or humans.
        Zombies can move 4 directions. Humans can move 8 directions.

        Return:
            tuple, possible moves for humans and zombies. 
        """
        def get_human_routs(neighbor_cells, distances, current_cell):
            """
            Returns a possible move for a human. 
            """
            possible_moves = []
            #furthest = float('-inf')
            for row, col in list(neighbor_cells):
                neighbor_cell_distance = distances[row][col]
                current_cell_distance = distances[current_cell[0]][current_cell[1]]
                if neighbor_cell_distance > current_cell_distance and (row, col) not in self.__get_obstacle_list():
                    possible_moves = [(row, col)]
                    #furthest = neighbor_cell_distance

            return random.choice(possible_moves)
 

        def get_zombie_routs(neighbor_cells, distances, current_cell):#
            """
            Returns a possible move for a zombie.
            """
            possible_moves = []
            closest = float('inf')
           
            # Add neighbor cells to the possible moves list if their distances are 
            # shorter than the current distance. 
            for row, col in list(neighbor_cells):
                neighbor_cell_distance = distances[row][col]
                current_cell_distance = distances[current_cell[0]][current_cell[1]]
                
                if neighbor_cell_distance < current_cell_distance and (row, col) not in self.__get_obstacle_list():
                    possible_moves = [(row, col)]
                    closest = distances[current_cell[0]][current_cell[1]]

            # If there was never a closer neighbor than the current cell then
            # the zombie is eating the human. It should stay in the same place
            if closest == float('inf'):
                possible_moves = [current_cell]

            return random.choice(possible_moves)
 
        # Dictionary for calling the proper subroutine and neighbors method.
        routs = {HUMAN : [get_human_routs, self.eight_neighbors], 
                 ZOMBIE: [get_zombie_routs, self.four_neighbors]}

        # Return a move for humans or zombies
        return routs[entity][0](routs[entity][1](current_cell[0], current_cell[1]), distances, current_cell)


    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        humans = list(self.__get_human_list())
        for human in humans:
            move = self.__get_move(zombie_distance, HUMAN, human) 
            self._human_list.remove((human))
            self.add_human(move[0], move[1])
 
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        print self.__str__()
        zombies = list(self.__get_zombie_list())
        for zombie in zombies:
            move = self.__get_move(human_distance, ZOMBIE, zombie) 
            self._zombie_list.remove((zombie))
            self.add_zombie(move[0], move[1])
        print 
        print self.__str__()


#import poc_zombie_apocalypse_testsuite2 as test
#test.phase1_test(Zombie)
#test.phase2_test(Zombie)
#test.phase3_test(Zombie)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))

