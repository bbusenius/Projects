"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster
#import cProfile
#import sys 

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    distance, point1, point2 = (float('inf'), -1, -1)
    retval = set([])

    idx1 = 0
    for dummy_cluster1 in cluster_list:
        idx2 = 0
        for dummy_cluster2 in cluster_list:
            if idx1 != idx2:
                dist, pt1, pt2 = pair_distance(cluster_list, idx1, idx2)
                if dist < distance:
                    distance, point1, point2 = dist, pt1, pt2
                    retval = set([(dist, point1, point2)])    
                elif dist == distance:
                    retval.add((dist, pt1, pt2)) 
            idx2 += 1 
        idx1 += 1
    return retval

def _compute_vert_lists(h_left, h_right, vert_order):
    """
    Copies in order the elements of h_left and h_right to v_left and v_right.

    Args:
        h_left: the left half of the horizontal incicies sorted in order.

        h_right: the right half of the horizontal indicies sorted in order.

        vert_order: the vertical order of indicies.

    Returns:
        A tupal with the left and right halves of the vertical indicies sorted
        in order.
    """
    v_left = []
    v_right = []
    for val in vert_order:
        if val in h_left:
            v_left.append(val)
        elif val in h_right:
            v_right.append(val) 
    return (v_left, v_right) 


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        # Base case
        total = len(horiz_order)
        if total <= 3:
            retval = slow_closest_pairs(list(cluster_list[val] for val in horiz_order)).pop()
            return (retval[0], horiz_order[retval[1]], horiz_order[retval[2]])
        # Divide
        else:
            # Number of points in each half
            # Should be: ceiling(x) = [x] is the smallest integer not less than x ([] should be chopped off at the bottom)
            half_points = int(math.ceil(total / 2.0))

            # Horizontal coordinate of the vertical dividing line
            mid = .5 * (cluster_list[horiz_order[half_points - 1]].horiz_center() + cluster_list[horiz_order[half_points]].horiz_center())

            # Split the horiz_order list into 2 halves
            h_left = horiz_order[0:half_points]
            h_right = horiz_order[half_points:total]

            # Copy in order the elements of h_left and h_right to v_left and v_right
            v_left, v_right = _compute_vert_lists(set(h_left), set(h_right), vert_order)

            # Recursion table
            recursion = {'left'  : fast_helper(cluster_list, h_left, v_left), 
                         'right' : fast_helper(cluster_list, h_right, v_right)}

            # Get the shortest distance based on the first element of the tuple
            if recursion['left'][0] < recursion['right'][0]:       
                dist, x_idx, y_idx = recursion['left']
            else:
                dist, x_idx, y_idx = recursion['right']

            # Conquer
            point_list = []
            extra_points = 0
            for element in vert_order:
                if abs(cluster_list[element].horiz_center() - mid) < dist:
                    point_list.append(element)
                    extra_points += 1
            for unum in range(0, extra_points - 1):
                for vnum in range(unum + 1, min([unum + 3, extra_points])):
                    if dist < pair_distance(cluster_list, point_list[unum], point_list[vnum])[0]: 
                        dist, x_idx, y_idx = dist, x_idx, y_idx
                    else:
                        dist = pair_distance(cluster_list, point_list[unum], point_list[vnum])[0]
                        x_idx = point_list[unum]
                        y_idx = point_list[vnum]
            
        
        return (dist, x_idx, y_idx)            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))




def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    https://d396qusza40orc.cloudfront.net/algorithmicthink/AT-Homework3/HierarchicalClustering.jpg
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    print type(cluster_list) 
    return []


    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    # initialize k-means clusters to be initial clusters with largest populations

    return []


