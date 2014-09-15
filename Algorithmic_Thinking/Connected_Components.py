"""
Connected components and graph resilience.
1. Implements a breadth-first search.
2. Compute connected components (CCs) of an undirected graph.
3. Determine the size of a graph's largest connected component.
4. Compute the resilience of a graph (measured by the size of its 
   largest connected component) as a sequence of nodes are deleted 
   from the graph.
"""
# Queue module
from collections import deque

# Additional graph functions and test data
import Degree_Distributions as dd

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

    while len(queue) != 0:
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
    remaining_nodes = ugraph.keys()
    connected_components = []
    while len(remaining_nodes) != 0:
        # Arbitrary node in remaining nodes
        arb_node = remaining_nodes.pop(0)
        nodes = bfs_visited(ugraph, arb_node)
        if nodes not in connected_components:
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

#bfs_visited(dd.EX_GRAPH1, 0)
#cc_visited(dd.EX_GRAPH1)
#print dd.EX_GRAPH1
#print largest_cc_size(dd.EX_GRAPH1)
compute_resilience(dd.EX_GRAPH1, [1, 4])
