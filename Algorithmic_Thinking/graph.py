"""
Degree distributions for graphs:
Sample python dictionaries representing simple directed graphs. 
Short functions that compute information about the distribution 
of the in-degrees for nodes in these graphs.
"""

# General imports
import urllib2
import random
import time

# Collections modules
from collections import deque
from collections import Counter as count

# DPA trial class
import alg_dpa_trial

# UPA trial class
import alg_upa_trial

# Example directed graphs
EX_GRAPH0 = {0 : set([1, 2]), 1 : set([]), 2 : set([])}

EX_GRAPH1 =  { 0 : set([1, 4, 5]), 
               1 : set([2, 6]), 
               2 : set([3]),
               3 : set([0]), 
               4 : set([1]), 
               5 : set([2]),
               6 : set([])}

EX_GRAPH2 =  { 0 : set([1, 4, 5]), 
               1 : set([2, 6]), 
               2 : set([3, 7]),
               3 : set([7]), 
               4 : set([1]), 
               5 : set([2]),
               6 : set([]),
               7 : set([3]), 
               8 : set([1, 2]),
               9 : set([0, 3, 4, 5, 6, 7])}

# Example undirected graphs
EX_GRAPH3 = { 0 : set([1, 3, 4]),
              1 : set([0, 2, 3, 4]),
              2 : set([1]),
              3 : set([0, 1]),
              4 : set([0, 1])}


def load_graph(graph_url):
    """
    Function that loads the text representation of a graph.
    Can be used on both directed and undirected graphs represented
    as adjacency lists. 
    
    Args: 
        graph_url: string url of a graph where the graph 
        is represented by space delimited numbers the first of 
        which is a node name and the following numbers are out
        edges e.g. 9306065 9207017 9203013 (9306065 is a node 
        and the other numbers are out-degree edges from 
        that node).
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def make_complete_graph(num_nodes):
    """
    Function returns a dictionary corresponding to a complete 
    graph with the specified number of nodes. A complete graph 
    contains all possible edges subject to the restriction that 
    self-loops are not allowed. Returns a dictionary corresponding 
    to an empty graph if num_nodes is negative. Since graphs are
    complete this can be used to create both directed and undirected
    graphs.

    Args:
        num_nodes: integer, the number of nodes in the graph.

    Returns: 
        A dictionary representation of a complete directed graph
        with the maximum number of edges. 
    """
    graph = {}
    for key in range(num_nodes):
        graph[key] = set([value for value in range(num_nodes) if value != key])
    return graph

def compute_in_degrees(digraph):
    """
    Function takes a directed graph digraph (represented as a dictionary) 
    and computes the in-degrees for the nodes in the graph.

    Args:
        digraph: dictionary representation of a directed graph.

    Returns:
        A dictionary with the same node keys as the original graph with 
        the in-degrees computed for each node.
    """
    in_degrees = {}
    for key in digraph:
        if not in_degrees.has_key(key):
            in_degrees[key] = 0
        for value in list(digraph[key]):
            if not in_degrees.has_key(value):
                in_degrees[value] = 1
            elif in_degrees.has_key(value):
                in_degrees[value] += 1 
            else:
                in_degrees[value] = 0
    return in_degrees

def in_degree_distribution(digraph):
    """
    Function takes a dictionary representation of a directed graph where the
    keys are primary nodes and the values are sets of out-degree nodes connected
    by edges from the primary nodes. This function computes the unnormalized 
    distribution of the in-degrees of the graph.

    Args:
        digraph: dictionary representation of a directed graph.

    Returns:
        A dictionary whose keys correspond to in-degrees of nodes in the graph. 
        The value associated with each particular in-degree is the number of 
        nodes with that in-degree. In-degrees with no corresponding nodes in 
        the graph are not included in the dictionary. 
    """
    in_degrees = compute_in_degrees(digraph)
    distribution = {}
    for key in in_degrees:
        if not distribution.has_key(in_degrees[key]):
            distribution[in_degrees[key]] = 1
        elif distribution.has_key(in_degrees[key]):
            distribution[in_degrees[key]] += 1
    return distribution

def get_graph_out_degrees(digraph):
    """
    Function takes a dictionary representation of a directed graph where the
    keys are primary nodes and the values are sets of out-degree nodes connected
    by edges from the primary nodes. This function computes the unnormalized 
    distribution of the out-degrees of the graph.

    Args:
        digraph: dictionary representation of a directed graph.

    Returns:
        A dictionary whose keys correspond to out-degrees of nodes in the graph. 
        The value associated with each particular out-degree is the number of 
        nodes with that out-degree.  
    """
    distribution = {}
    for node in digraph:
        # Out-degree for each node
        out_degree = len(digraph[node])
        if not distribution.has_key(out_degree): 
            distribution[out_degree] = 1
        elif distribution.has_key(out_degree):
            distribution[out_degree] += 1
    return distribution


def get_node_out_degrees(node):
    """
    Computes the number of out degrees of a specific 
    node in a directed graph.
    
    Args:
        node: a set of out-degrees for a given node
    """
    return len(node)


def sort_dict(dictionary):
    """
    Sort a dictionary by key.

    Args:
        dictionary: a dictionary to sort

    Returns:
        A list of tuples as key value pairs ordered by key.
    """
    retval = []
    for key in sorted(dictionary.iterkeys()):
        retval.append((key, dictionary[key]))
    return retval


def normalize_distribution(dictionary):
    """
    Function normalizes the degree distribution of a graph.

    Args:
        dictionary: a dictionary of key value pairs where 
        the keys represent degrees and the values represent
        the number of nodes with the stated degree. Such a
        dictionary can be computed by the 
        in_degree_distribution function.

    Returns:
        A dictionary of degrees with normalized distributions
        that sum up to 1.
    """
    retval = {}
    num_nodes =  float(sum(dictionary.values()))
    for key in dictionary:
        retval[key] = dictionary[key] / num_nodes
    return retval


def average_out_degree_dist(digraph):
    """
    Calculate the average out degree distribution of 
    a directed graph.
    
    Args:
        A dictionary representation of the out-degree 
        distribution of a directed graph where keys are
        and values are sets of out degree edges.
        out-degrees and values are the numbers of nodes
        with the given out-degree in the key (the 
        out_degree_distribution function creates such 
        a dictionary for a directed graph).
    """
    total = []
    [total.append(len(digraph[node])) for node in digraph]
    return float(sum(total)) / len(digraph)
        

def random_undirected_graph(num_nodes, probability):
    """
    Algorithm for generating random undirected graphs
    (ER algorithm) where edges between nodes are created
    with equal probability.
    """
    # All possible nodes 
    all_nodes = range(num_nodes)

    # Dynamically create a graph
    graph = {}
    for key in range(num_nodes):
        graph[key] = set([])

    # Loop over every possible combination of 
    # nodes and build an edge between them 
    # based on the probability
    for current_node in range(num_nodes):
        for possible_node in all_nodes:
            if possible_node != current_node:
                a = random.uniform(0, 1.0)
                if a < probability:
                    graph[current_node].add(possible_node)
    return graph

def random_directed_graph(num_nodes, probability):
    """
    Algorithm for generating random directed graphs 
    (Modified ER algorithm) where edges between nodes are created
    with equal probability.
    """
    def random_num():
        """
        Return a random number.
        """
        return random.uniform(0, 1.0)

    # All possible nodes 
    all_nodes = range(num_nodes)

    # Dynamically create a graph without edges
    graph = {}
    for key in range(num_nodes):
        graph[key] = set([])

    # Loop over every possible combination of 
    # nodes and build an edge between them 
    # based on the probability
    for current_node in range(num_nodes):
        for possible_node in all_nodes:
            if possible_node != current_node:
                a = random_num()
                if a < probability:
                    graph[current_node].add(possible_node)
                b = random_num()
                if b < probability:
                     graph[possible_node].add(current_node)
    return graph


def random_DPA_directed_graph(num_nodes, m_nodes):
    """
    Function uses the Directed Preferential Attachment algoritm (DPA algorithm) 
    to create a random directed graph. The DPA algorithm sets edges based on a 
    preferential attachment mechanism giving more edges to nodes created earlier 
    in the simulation.

    Args:
        num_nodes: integer, the numbe of nodes to be in the graph.
        
        m_nodes: integer,  the number of existing nodes to 
        which a new node is connected during each iteration.

    Returns:
        A dictionary representation of a directed graph where keys are node names
        and values are sets of out degree edges.
    """
    # Create an instance of DPATrial
    dpa_obj = alg_dpa_trial.DPATrial(m_nodes) 

    # Make a complete digraph with m nodes and add it to the final output
    graph = make_complete_graph(m_nodes)

    for node in range(m_nodes, num_nodes):
        neighbors = dpa_obj.run_trial(m_nodes)
        graph[node] = neighbors
    return graph


def random_UPA_undirected_graph(num_nodes, m_nodes):
    """
    Function uses the Undirected Preferential Attachment algoritm (UPA algorithm) 
    to create a random undirected graph. The UPA algorithm sets edges based on a 
    preferential attachment mechanism giving more edges to nodes created earlier 
    in the simulation.

    Args:
        num_nodes: integer, the numbe of nodes to be in the graph.
        
        m_nodes: integer,  the number of existing nodes to 
        which a new node is connected during each iteration.

    Returns:
        A dictionary representation of an undirected graph where keys are node names
        and values are sets of neighbors.
    """
    # Create an instance of UPATrial
    upa_obj = alg_upa_trial.UPATrial(m_nodes) 

    # Make a complete ugraph with m nodes and add it to the final output
    graph = make_complete_graph(m_nodes)

    for node in range(m_nodes, num_nodes):
        # Add neighbors to nodes
        neighbors = upa_obj.run_trial(m_nodes)
        graph[node] = neighbors
        # Add nodes to neighbors 
        for n in neighbors:
            graph[n].add(node)
    return graph


#########################################################################
#########################################################################

"""
Connected components and graph resilience.
1. Implements a breadth-first search.
2. Compute connected components (CCs) of an undirected graph.
3. Determine the size of a graph's largest connected component.
4. Compute the resilience of a graph (measured by the size of its 
   largest connected component) as a sequence of nodes are deleted 
   from the graph.
"""

def bfs_visited(ugraph, start_node): 
    """
    A breadth-first search for finding a set of all 
    connected components of an undirected graph.

    Args:
        ugraph: a dictionary of sets representing an 
        undirected graph.

        start_node: integer, the node to start at.

    Returns:
        A set consisting of all nodes visited by a 
        breadth-first search beginning at start_node.
    """
    # Initialize an empty queue.
    queue = deque()  

    # All nodes visited by the algorithm.
    visited = set([start_node])
   
    # Add the start node to the queue 
    queue.append(start_node)

    while queue:
        # Dequeue
        current_node = queue.popleft()
        
        # Iterate neighbors of the current node.
        for neighbor in ugraph[current_node]:
            # If the neighbor isn't in the visited set
            if neighbor not in visited:
                # Add neighbor to visited and queue
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def cc_visited(ugraph):
    """
    Takes and undirected graph and returns a list of sets, 
    where each set consists of all the nodes (and nothing else) 
    in a connected component, and there is exactly one set in 
    the list for each connected component in ugraph and nothing else.

    Args: 
        ugraph: a dictionary of sets representing an 
        undirected graph.

    Returns:
        A list of sets.

    """
    remaining_nodes = set(ugraph.keys())
    connected_components = []
    while len(remaining_nodes) != 0:
        # Arbitrary node in remaining nodes
        arb_node = remaining_nodes.pop()
        nodes = bfs_visited(ugraph, arb_node)

        # Remove bfs nodes from remaining nodes to shorten the loop
        #remaining_nodes = list(n for n in remaining_nodes if n not in nodes)
        remaining_nodes = remaining_nodes - nodes
        connected_components.append(nodes)

    return connected_components

def largest_cc_size(ugraph):
    """
    Takes an undirected graph and returns the size (an integer) 
    of the largest connected component in the graph.

    Args:
        ugraph: a dictionary of sets representing an 
        undirected graph.

    Returns:
        integer, the size of the largest connected component.
    """
    largest = 0
    for node in cc_visited(ugraph):
        if len(node) > largest:
            largest = len(node)
    return largest

def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order 
    and iterates through the nodes in attack_order. For each node in 
    the list, the function removes the given node and its edges from 
    the graph and then computes the size of the largest connected 
    component for the resulting graph.

    Args:
        ugraph: a dictionary of sets representing an 
        undirected graph.

        attack_order: a list of nodes to remove from the graph 
        along with their edges.

    Returns:
        A list whose k+1th entry is the size of the largest connected 
        component in the graph after the removal of the first k nodes 
        in attack_order. The first entry (indexed by zero) is the size 
        of the largest connected component in the original graph. 
    """
    resilience = [largest_cc_size(ugraph)]
    for attack_node in attack_order:
        # Remove the attack_node from the graph
        ugraph.pop(attack_node)

        # Remove the edges for attack_node from all other nodes
        for node in ugraph:
            if attack_node in ugraph[node]:
                ugraph[node].remove(attack_node)

        # Append the next largest cc size to the return data
        resilience.append(largest_cc_size(ugraph))

    return resilience


def count_edges(graph, graph_type=''):
    """
    Counts the number of edges in a graph.

    Args:
        graph: a dictionary of sets representing a graph.

        graph_type: string, directed or undirected, the
        type of graph for which we are to count edges.

    Returns:
        integer, the number of edges in the graph.
    """
    count = 0
    for node in graph:
        count += len(graph[node])   
 
    if graph_type == 'directed':
         return count
    else:
        return count / 2

def random_order(graph):
    """
    Returns the nodes of a graph in a random order.

    Args:
        graph: a dictionary of sets representing a graph.
    """
    nodes = graph.keys()
    random.shuffle(nodes)
    return nodes

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph.

    Args:
        ugraph: a dictionary of sets representing an 
        undirected graph.

    Returns:
        None, deletes a node from the graph.
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

def targeted_order(ugraph):
    """
    DEPRECATED - Currently fails for some reason.
    Compute a targeted attack order consisting
    of nodes of maximal degree.
    
    Args:
        ugraph: a dictionary of sets representing an 
        undirected graph.

    Returns:
        A list of nodes.
    """
    # Copy the graph.
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def fast_targeted_order(ugraph):
    """
    A faster implementation of targeted_order.
    Compute a targeted attack order consisting
    of nodes of maximal degree.
    
    Args:
        ugraph: a dictionary of sets representing an 
        undirected graph.

    Returns: 
        A list of nodes in decreasing order of their
        degrees.
    """
    # Copy the graph
    new_graph = copy_graph(ugraph)

    # Create a list whose kth element is the set of nodes of degree k.
    # Put the list in order of decreasing degree.
    degree_sets = list(set([]) for degree_node in range(len(new_graph)))
    l = list(degree_sets[len(new_graph[degree_node])].add(degree_node) for degree_node in new_graph)
    degree_sets = degree_sets[::-1]

    retval = []
    for nodes in degree_sets:
        while len(nodes) != 0:
            current_node = nodes.pop()
            retval.append(current_node) 
    return retval
