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
        cells = [ [self._grid_width * self._grid_height for row in range(self._grid_height)] for col in range(self._grid_width)] 
        for row, col in self.get_human_list():
            cells[row][col] = "H"
        for row, col in self.get_zombie_list():
            if (row, col) in self.get_human_list():
                cells[row][col] = "E"
            else:
                cells[row][col] = "Z"
        for row, col in self.get_obstacle_list():
            cells[row][col] = "O" 

        string = str(cells) 
        string = string.replace("[[", " [")
        string = string.replace("]]", "]")
        string = string.replace("],", "]\n")
          
        return string 
 
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
        while boundary.__len__() > 0:
            neighbor_cells = []
            current_cell = boundary.dequeue()
            neighbor_cells.extend(self.four_neighbors(current_cell[0], current_cell[1]))
            # Distance is the position of the current cell + 1 (incrementing is not necessary)
            distance = distance_field[current_cell[0]][current_cell[1]] + 1
            for row, col in neighbor_cells:
                # If there isn't an obstacle
                # if self.is_empty(row, col):
                if (row, col) not in self.get_obstacle_list():
                    # If the cell hasn't been visited
                    if visited.is_empty(row, col) :
                        visited.set_full(row, col)
                        distance_field[row][col] = distance
                        boundary.enqueue((row, col))
        return distance_field 

    
    #def get_moves(self, distances, entity, row, col):
        """
        Method gets possible routs for zombies or humans.
        Zombies can move 4 directions. Humans can move 8 directions.

        Return:
            list: of possible moves for zombies or humans. 
        """
        """routs = {HUMAN : [self.get_human_routs, self.eight_neighbors], 
                 ZOMBIE: [self.get_zombie_routs, self.four_neighbors]}

        return routs[entity][0](routs[entity][1](row, col), distances, (row, col))"""

    
    def get_human_routs(self, routs, distances, current_cell):
        """
        Args:
            routs: tuple (row, cell), the neighbor cells to where
            humans can move. Humans are allowed to move in 8 directions.

            distances: grid list of lists. The calculated distances 
print 
            between humans and zombies.
        """
        current_distances = self.compute_distance_field(HUMAN)
        possible_moves = [(float('-inf'), float('-inf'))]
        furthest = float('-inf')

        for row, col in routs:
            if distances[row][col] < furthest:
                pass
            elif distances[row][col] > current_distances[row][col]:
                possible_moves = [(row, col)]
                furthest = distances[row][col]
            elif distances[row][col] == possible_moves[0]:
                possible_moves.append((row, col))
        return possible_moves

    
    def get_zombie_routs(self, routs, distances, current_cell):
        """
        Args:
            routs: tuple (row, cell), the neighbor cells to where
            zombies can move. Zombies are allowed to move in 4 directions.

            distances: grid list of lists. The calculated distances 
            between humans and zombies.#
        """
        # Current distance to human
        current_distances = self.compute_distance_field(ZOMBIE)
        possible_moves = [(float('-inf'), float('-inf'))]
        closest = float('inf')
        for row, col in routs:
            # If the distance is further than the current 
            # possible closest move don't do anything
            if distances[row][col] > closest:
                pass
            # If distance to the human is less than current 
            # distance to the human, make this the possible move
            elif distances[row][col] < current_distances[row][col]:
                possible_moves = [(row, col)]
                closest = distances[row][col]
            # If distance to the human is the same as the current 
            # the distance of the current possible move, add this 
            # move to the list of possible moves as well
            elif distances[row][col] == possible_moves[0]:
                possible_moves.append((row, col))
            # If there aren't any good moves, the zombie should
            # stay in its current position
            else:
                possible_moves = [current_cell]
    
        # Return a list of possible moves
        return possible_moves

    
    #def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        # 1. Set variables: victims (queue of humans being chased), distances (curor current_distances[row][col] == 0rent
        # distances between humans and zombies) current_cell, escape_routs, possible_move.
        """entities = poc_queue.Queue()
        dummy_entities = [entities.enqueue(human) for human in self.get_entity_list(HUMAN)]

        while entities.__len__() > 0:
            current_cell = entities.dequeue()
            moves = self.get_moves(zombie_distance, HUMAN, current_cell[0], current_cell[1])

            # 3. Randomly choose one member of the possible_moves list and use it
            # to update the self._human_list. 
            choice = random.choice(moves)
            self._human_list.remove(current_cell)
            self.add_human(choice[0], choice[1])"""
             
    
    #def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        # 1. Set variables: victims (queue of humans being chased), distances (current
        # distances between humans and zombies) current_cell, escape_routs, possible_move.
        """entities = poc_queue.Queue()
        dummy_entities = [entities.enqueue(zombie) for zombie in self.get_entity_list(ZOMBIE)]

        while entities.__len__() > 0:
            current_cell = entities.dequeue()
            moves = self.get_moves(human_distance, ZOMBIE, current_cell[0], current_cell[1])

            # 3. Randomly choose one member of the possible_moves list and use it
            # to update the self._zombie_list. 
            choice = random.choice(moves)
            self._zombie_list.remove(current_cell) 
            self.add_zombie(choice[0], choice[1])"""


    def get_move(self, distances, entity, current_cell):
        """
        Method gets possible routs for zombies or humans.
        Zombies can move 4 directions. Humans can move 8 directions.

        Return:
            list: of possible moves for zombies or humans. 
        """
        def get_human_routs(neighbor_cells, distances, current_cell):
            """
            Gets a move for a human and updates the human list.
            """
            possible_moves = []
            furthest = float('-inf')
            for row, col in neighbor_cells:
                neighbor_cell_distance = distances[row][col]
                current_cell_distance = distances[current_cell[0]][current_cell[1]]
                if neighbor_cell_distance > furthest and (row, col) not in self.get_obstacle_list():
                    possible_moves = [(row, col)]
                    furthest = neighbor_cell_distance

            return random.choice(possible_moves)
 

        def get_zombie_routs(neighbor_cells, distances, current_cell):#
            """
            Gets a move for a zombie and updates the zombie list.
            """
            possible_moves = []
            closest = float('inf')
            #print "DIST", distances
            #print "OBS", self.get_obstacle_list()
            #print "NEIGH", neighbor_cells 
            #print "CURRENT CELL", current_cell      
            for row, col in neighbor_cells:
                neighbor_cell_distance = distances[row][col]
                current_cell_distance = distances[current_cell[0]][current_cell[1]]
                if neighbor_cell_distance < closest and (row, col) not in self.get_obstacle_list() and current_cell_distance != 0:
                    possible_moves = [(row, col)]
                    closest = neighbor_cell_distance
                else:
                    possible_moves = [current_cell]

            return random.choice(possible_moves)
 
        routs = {HUMAN : [get_human_routs, self.eight_neighbors], 
                 ZOMBIE: [get_zombie_routs, self.four_neighbors]}

        return routs[entity][0](routs[entity][1](current_cell[0], current_cell[1]), distances, current_cell)


    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        humans = list(self.get_human_list())
        for human in humans:
            move = self.get_move(zombie_distance, HUMAN, human) 
            self._human_list.remove((human))
            self.add_human(move[0], move[1])
 
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        #print self.__str__()
        zombies = self.get_zombie_list()
        for zombie in zombies:
            move = self.get_move(human_distance, ZOMBIE, zombie) 
            self._zombie_list.remove((zombie))
            self.add_zombie(move[0], move[1])
        
        #print self.__str__()


#import poc_zombie_apocalypse_testsuite2 as test
#test.phase1_test(Zombie)
#test.phase2_test(Zombie)
#test.phase3_test(Zombie)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))

