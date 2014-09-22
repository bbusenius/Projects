"""
Simulate a cyber attack on different kinds of computer networks represented 
by three different kinds of undirected graphs.

1. An example computer network.
2. A network based on the ER algorithm (Erdos and Renyi) that sets an edge 
   between each pair of nodes with equal probability.
3. A network based on the UPA, Undirected Preferential Attachment algoritm
   that sets edges based on a preferential attachment mechanism giving priority
   to nodes created earlier in the simulation.
"""

# Graph library
import graph as g

# Plot library
import matplotlib.pyplot as plt

# Profile for troubleshooting
import cProfile

# URL of the network graph
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt" 

#print g.count_edges(g.load_graph(NETWORK_URL))
#print g.count_edges(g.random_undirected_graph(1347, .0034))
#print g.count_edges(g.random_UPA_undirected_graph(1347, 2))
#print g.random_order(g.load_graph(NETWORK_URL))

def plot_random_attack_res():
    """
    Function plots the computed resilience of three networks 
    represented as undirected graphs as they undergo a random 
    attack sequence.

    1. A real computer network.
    2. A simulated network built using the ER algorithm.
    3. A simulated network built using the UPA algorithm.
    """

    # Load three different graphs
    network_graph = g.load_graph(NETWORK_URL)
    er_graph = g.random_undirected_graph(1347, .0034)
    upa_graph = g.random_UPA_undirected_graph(1347, 2)

    # Compute resilience for the three graphs
    network_res = g.compute_resilience(network_graph, g.random_order(network_graph))
    er_res = g.compute_resilience(er_graph, g.random_order(er_graph))
    upa_res = g.compute_resilience(upa_graph, g.random_order(upa_graph))

    plt.plot(network_res, '-b', label='Computer network')
    plt.plot(er_res, '-r', label='ER graph, p = .0034')
    plt.plot(upa_res, '-y', label='UPA graph, m = 2')
    plt.legend(loc='upper right')
    plt.title('Network resilience in a random attack sequence')
    plt.ylabel('Largest connected component')
    plt.xlabel('Number of nodes removed')
    plt.show()

def plot_targeted_attack_res():
    """
    Function plots the computed resilience of three networks 
    represented as undirected graphs as they undergo an attack
    sequence that eliminates nodes in descending order of 
    connectivity (most highly connected nodes are eliminated first).

    1. A real computer network.
    2. A simulated network built using the ER algorithm.
    3. A simulated network built using the UPA algorithm.
    """

    # Load three different graphs
    network_graph = g.load_graph(NETWORK_URL)
    er_graph = g.random_undirected_graph(1347, .0034)
    upa_graph = g.random_UPA_undirected_graph(1347, 2)

    # Compute resilience for the three graphs
    network_res = g.compute_resilience(network_graph, g.fast_targeted_order(network_graph))
    er_res = g.compute_resilience(er_graph, g.fast_targeted_order(er_graph))
    upa_res = g.compute_resilience(upa_graph, g.fast_targeted_order(upa_graph))

    plt.plot(network_res, '-b', label='Computer network')
    plt.plot(er_res, '-r', label='ER graph, p = .0034')
    plt.plot(upa_res, '-y', label='UPA graph, m = 2')
    plt.legend(loc='upper right')
    plt.title('Network resilience in a targeted attack sequence')
    plt.ylabel('Largest connected component')
    plt.xlabel('Number of nodes removed')
    plt.show()

def legend_example():
    """
    Plot an example with two curves and legends
    """
    xvals = [1, 2, 3, 4, 5]
    yvals1 = [1, 2, 3, 4, 5]
    yvals2 = [1, 4, 9, 16, 25]

    plt.plot(xvals, yvals1, '-b', label='linear')
    plt.plot(xvals, yvals2, '-r', label='quadratic')
    plt.legend(loc='upper right')
    plt.show()

#print g.targeted_order(g.EX_GRAPH3)
#print g.fast_targeted_order(g.EX_GRAPH3)
plot_random_attack_res()
#plot_targeted_attack_res()


#network_graph = g.load_graph(NETWORK_URL)
#cProfile.run('g.targeted_order(network_graph)')
#cProfile.run('g.fast_targeted_order(network_graph)')
