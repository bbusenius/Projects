"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster
import matplotlib.pyplot as plt

# conditional imports
if DESKTOP:
    import alg_project3_template as alg_project3_solution # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_896_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    #cluster_list = sequential_clustering(singleton_list, 15)    
    #print "Displaying", len(cluster_list), "sequential clusters"

    cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 50)
    print "Displaying", len(cluster_list), "hierarchical clusters"

    #cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 20, 5)   
    #print "Displaying", len(cluster_list), "k-means clusters"

    print 'Calculating distortion...'
    print alg_project3_solution.compute_distortion(cluster_list, data_table)
    
            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)


def get_distortions(start, end, data, alg):
    """
    Function computes the distortions for clusters ranging from 
    start to end (inclusive).

    Args:
        start: integer, the number of clusterings to begin with.

        end: integer, the number of clusterings to stop at.

        data: which data set to use (111, 290, 896, 3108)

        alg: string, the type of algorithm to test (k-smean or hierarchical)

    Returns:
        A list distortions for clusters ranging from start to end (inclusive).
    """
    lookup = {'111' : DATA_111_URL, 
              '290' : DATA_290_URL ,
              '896' : DATA_896_URL,
              '3108' : DATA_3108_URL}

    data_table = load_data_table(lookup[data])
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
       
    distortions = []
    for num in range(start, end + 1):

        if alg == 'kmeans':
            cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, num, 5)
        elif alg == 'hierarchical':
            cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, num)

        distortions.append(alg_project3_solution.compute_distortion(cluster_list, data_table))
        print 'Calculating distortion...'
    return distortions 


def plot_distortions(start, end, data, title='', xlabel='', ylabel=''):
    """
    Plots the distortions for k-means and hierarchical clustering methonds 
    on clusterings from start number to end number.  
    """
    title = title + ' on the ' + data + ' data set' 
    
    kmeans = get_distortions(start, end, data, 'kmeans')
    hierarchical = get_distortions(start, end, data, 'hierarchical')
    plt.plot(kmeans, '-r', label='K-means')
    plt.plot(hierarchical, '-b', label='Hierarchical')

    # Add attributes to the plot
    plt.legend(loc='upper right')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


#plot_distortions(6, 20, '111', title='Distortion of clusters', xlabel='Output clusters', ylabel='Distortions')
#plot_distortions(6, 20, '290', title='Distortion of clusters', xlabel='Output clusters', ylabel='Distortions')
#plot_distortions(6, 20, '896', title='Distortion of clusters', xlabel='Output clusters', ylabel='Distortions')

run_example()
