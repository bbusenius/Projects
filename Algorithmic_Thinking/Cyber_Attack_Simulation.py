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

import cProfile

# URL of the network graph
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt" 

#print g.count_edges(g.load_graph(NETWORK_URL))
#print g.count_edges(g.random_undirected_graph(1347, .0034))
#print g.count_edges(g.random_UPA_undirected_graph(1347, 2))
#print g.random_order(g.load_graph(NETWORK_URL))

# Load three different graphs
network_graph = g.load_graph(NETWORK_URL)
#er_graph = g.random_undirected_graph(1347, .0034)
#upa_graph = g.random_UPA_undirected_graph(1347, 2)


#cProfile.run('g.largest_cc_size(network_graph)')
#cProfile.run('g.random_order(network_graph)')
x = g.random_order(network_graph)
cProfile.run('g.compute_resilience(network_graph, x)')


# Compute resilience for the three graphs
network_res = g.compute_resilience(network_graph, g.random_order(network_graph))
#er_res = g.compute_resilience(er_graph, g.random_order(er_graph))
#upa_res = g.compute_resilience(upa_graph, g.random_order(upa_graph))
