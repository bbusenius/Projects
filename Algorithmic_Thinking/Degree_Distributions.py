"""
Degree distributions for graphs:
Sample python dictionaries representing simple directed graphs. 
Short functions that compute information about the distribution 
of the in-degrees for nodes in these graphs.
"""

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


def make_complete_graph(num_nodes):
    """
    Function returns a dictionary corresponding to a complete 
    directed graph with the specified number of nodes. A complete 
    graph contains all possible edges subject to the restriction 
    that self-loops are not allowed. Returns a dictionary corresponding 
    to an empty graph if num_nodes is negative.

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
    Function takes a directed graph digraph (represented as a dictionary) 
    and computes the unnormalized distribution of the in-degrees of the graph.

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

