"""
Degree distributions for graphs:
Sample python dictionaries representing simple directed graphs. 
Short functions that compute information about the distribution 
of the in-degrees for nodes in these graphs.
"""

# general imports
import urllib2
import random
import time

# Plotting library
import matplotlib.pyplot as plt

# DPA trial class
import alg_dpa_trial

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


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Args: 
        graph_url: string url of a digraph where the digraph 
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


###############################################################3


def plot_citation_graph():
    """
    Function for plotting the in-degree distribution of 
    a specific citation graph.
    """
    # Load the external graph of citation information
    citation_graph = load_graph(CITATION_URL)

    # Calculate the in-degree distribution of the citation graph
    in_degree_dist = in_degree_distribution(citation_graph)

    # Normalize the in-degree distribution to sum up to 1
    normalized_distribution = normalize_distribution(in_degree_dist)

    # Plot the normalized distribution on a log/log graph
    plt.loglog(normalized_distribution.keys(), normalized_distribution.values(), 'ro', basex=10, basey=10)
    plt.title('Log/log plot of the normalized distribution of a citation graph')
    plt.ylabel('Number of citations - base 10')
    plt.xlabel('Papers - base 10')
    plt.show()

def average_out_degree_dist(digraph):
    """
    Calculate the average out degree distribution of 
    a directed graph.
    
    Args:
        A dictionary representation of the out-degree 
        distribution of a directed graph where keys are
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
    (ER algorithm).
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
    (Modified ER algorithm).
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

def plot_graph(graph, title='', xlabel='', ylabel=''):
    """
    Function uses matplotlib to create a log/log plot of the 
    in-degree distribution of a graph.

    Args: 
        graph: a dictionary representation of a directed graph
        where the keys are node names and the values are sets
        of edges.

    Returns:
        None and plots a log/log plot of the graph.
    """
    # Calculate the in-degree distribution of the graph
    in_degree_dist = in_degree_distribution(graph)

    # Normalize the in-degree distribution to sum up to 1
    normalized_distribution = normalize_distribution(in_degree_dist)

    # Plot the normalized distribution on a graph
    #plt.plot(normalized_distribution.keys(), normalized_distribution.values(), 'ro') 
    plt.loglog(normalized_distribution.keys(), normalized_distribution.values(), 'bo', basex=10, basey=10)

    # Add attributes to the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def random_DPA_directed_graph(num_nodes, m_nodes):
    """
    Function uses the DPA algorithm to create a random
    directed graph.

    Args:
        num_nodes: integer, the numbe of nodes to be in the graph.
        
        m_nodes: integer,  the number of existing nodes to 
        which a new node is connected during each iteration.
    """
    # Create an instance of DPATrial
    dpa_obj = alg_dpa_trial.DPATrial(m_nodes) 

    # Make a complete digraph with m nodes and add it to the final output
    graph = make_complete_graph(m_nodes)

    for node in range(m_nodes, num_nodes):
        neighbors = dpa_obj.run_trial(m_nodes)
        graph[node] = neighbors
    return graph

#plot_graph(random_directed_graph(2770, 0.5), 'Log/log plot of the in-degree distribution of the ER graph', 'Nodes (base 10)', 'In-degrees (base 10)')
#plot_citation_graph()
#print average_out_degree_dist(load_graph(CITATION_URL))
#print make_complete_graph(4)
#print random_DPA_directed_graph(27770, 13)
#plot_graph(random_DPA_directed_graph(27770, 13), 'Log/log plot of the in-degree distribution of the DPA graph', 'Nodes (base 10)', 'In-degrees (base 10)')

