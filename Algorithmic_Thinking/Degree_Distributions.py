"""
Simulation for comparing the degree distribution of a scientific paper citation
graph with that of a randomly created directed graph based on the DPA algorithm
that sets edges between nodes preferentially. 
"""

# Graph library
import graph as g

# Plotting library
import matplotlib.pyplot as plt

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def plot_citation_graph():
    """
    Function for plotting the in-degree distribution of 
    a specific citation graph.
    """
    # Load the external graph of citation information
    citation_graph = g.load_graph(CITATION_URL)

    # Calculate the in-degree distribution of the citation graph
    in_degree_dist = g.in_degree_distribution(citation_graph)

    # Normalize the in-degree distribution to sum up to 1
    normalized_distribution = g.normalize_distribution(in_degree_dist)

    # Plot the normalized distribution on a log/log graph
    plt.loglog(normalized_distribution.keys(), normalized_distribution.values(), 'ro', basex=10, basey=10)
    plt.title('Log/log plot of the normalized distribution of a citation graph')
    plt.ylabel('Number of citations - base 10')
    plt.xlabel('Papers - base 10')
    plt.show()

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
    in_degree_dist = g.in_degree_distribution(graph)

    # Normalize the in-degree distribution to sum up to 1
    normalized_distribution = g.normalize_distribution(in_degree_dist)

    # Plot the normalized distribution on a graph
    #plt.plot(normalized_distribution.keys(), normalized_distribution.values(), 'ro') 
    plt.loglog(normalized_distribution.keys(), normalized_distribution.values(), 'bo', basex=10, basey=10)

    # Add attributes to the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

#plot_graph(g.random_directed_graph(2770, 0.5), 'Log/log plot of the in-degree distribution of the ER graph', 'Nodes (base 10)', 'In-degrees (base 10)')
#plot_citation_graph()
#print g.average_out_degree_dist(g.load_graph(CITATION_URL))
#print g.make_complete_graph(4)
#print g.random_DPA_directed_graph(27770, 13)
plot_graph(g.random_DPA_directed_graph(27770, 13), 'Log/log plot of the in-degree distribution of the DPA graph', 'Nodes (base 10)', 'In-degrees (base 10)')

