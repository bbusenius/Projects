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
    
    def get_obstacle_list(self):
        """
        Return a list of obstacles.
        """
        return self._obstacle_list

    def get_human_list(self):
        """
        Return a list of humans.
        """
        return self._human_list

    def get_zombie_list(self):
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
        entity_lists = { HUMAN  : list(self.get_human_list()),
                         ZOMBIE : list(self.get_zombie_list()) }

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
        distance = 1
        while boundary.__len__() > 0:
            neighbor_cells = []
            current_cell = boundary.dequeue()
            neighbor_cells.extend(self.four_neighbors(current_cell[0], current_cell[1]))
            for neighbor_cell in neighbor_cells:
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]) :
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance
                    boundary.enqueue(neighbor_cell)
            distance += 1
        return distance_field 

    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        pass
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        pass

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))

