"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# Library for reasoning about directed graphs
import Degree_Distributions as dd

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

# Plotting library
import matplotlib.pyplot as plt
import random 

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
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

def plot_citation_graph():
    """
    Function for plotting the citation graph.
    """
    # Load the external graph of citation information
    citation_graph = load_graph(CITATION_URL)

    # Calculate the in-degree distribution of the citation graph
    in_degree_distribution = dd.in_degree_distribution(citation_graph)

    # Normalize the in-degree distribution to sum up to 1
    normalized_distribution = dd.normalize_distribution(in_degree_distribution)

    # Plot the normalized distribution on a log/log graph
    plt.loglog(normalized_distribution.keys(), normalized_distribution.values(), 'ro', basex=10, basey=10)
    plt.title('Log/log plot of the normalized distribution of a citation graph')  
    plt.ylabel('Number of citations - base 10')  
    plt.xlabel('Papers - base 10')  
    plt.show()


def ER_algorithm(num_nodes, probability):

    # All possible nodes 
    all_nodes = range(num_nodes)

    # Dynamically create a graph
    graph = {}
    for key in range(num_nodes):
        graph[key] = []

    # Loop over every possible combination of 
    # nodes and build an edge between them 
    # based on the probability
    for current_node in range(num_nodes):
        for possible_node in all_nodes:
            if possible_node != current_node:
                a = random.uniform(0, 1.0)
                if a < probability:
                    graph[current_node].append(possible_node)
    return graph

print ER_algorithm(100, 0.4)

#plot_citation_graph()
