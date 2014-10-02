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
import cProfile
import sys 

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
            #small_list = []
            #for val in horiz_order:
            #    small_list.append(cluster_list[val])
            small_list = list(cluster_list[val] for val in horiz_order)
            #print 'TEST ########################################'
            #print slow_closest_pairs(small_list)
            return slow_closest_pairs(small_list).pop()
        # Divide
        else:
            # Number of points in each half
            # Should be: ceiling(x) = [x] is the smallest integer not less than x ([] should be chopped off at the bottom)
            half_points = int(math.ceil(total / 2.0))
            # Horizontal coordinate of the vertical dividing line
            mid = .5 * (cluster_list[horiz_order[0]].horiz_center() + cluster_list[horiz_order[total-1]].horiz_center())

            # Split the horiz_order list into 2 halves
            h_left = horiz_order[0:half_points]
            h_right = horiz_order[half_points:total]

            # Copy in order the elements of h_left and h_right to v_left and v_right
            #v_left = list(val for key, val in enumerate(vert_order) if val in h_left)
            #v_right = list(val for key, val in enumerate(vert_order) if val in h_right)
            v_left, v_right = _compute_vert_lists(set(h_left), set(h_right), vert_order)

            # Broken here <------might be a result of the bad merge 
            left = fast_helper(cluster_list, h_left, v_left)
            right = fast_helper(cluster_list, h_right, v_right)

            # Get the shortest distance based on the first element of the tuple
            if left[0] < right[0]:       
                dist, x_idx, y_idx = left[0], left[1], left[2]
            else:
                dist, x_idx, y_idx = right[0], right[1], right[2]

            # Conquer
            point_list = []
            extra_points = 0
            for element in vert_order:
                if element - mid < dist:
                    point_list.append(element)
                    extra_points += 1
            for unum in range(0, extra_points - 1):
                for vnum in range(unum + 1, min([unum + 3, extra_points])):
                    #dist, x_idx, y_idx = min((dist, x_idx, y_idx), (cluster_list[point_list[unum]].distance(cluster_list[point_list[vnum]]), point_list[unum], point_list[vnum]))
                    #print pair_distance(cluster_list, point_list[unum], point_list[vnum])
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


#print fast_closest_pair([alg_cluster.Cluster(set([]), 4, 2, 1, 0), alg_cluster.Cluster(set([]), 5, 1, 1, 0), alg_cluster.Cluster(set([]), 6, 2, 1, 0), alg_cluster.Cluster(set([]), 8, 2, 1, 0)]) 

#print slow_closest_pairs([alg_cluster.Cluster(set(['06111', '06083', '06059', '06037']), 105.658470671, 359.684551417, 13518171, 0.000103217153859), alg_cluster.Cluster(set(['06029', '06107']), 105.323760186, 318.981625973, 1029666, 8.30607041507e-05), alg_cluster.Cluster(set(['06071']), 148.402461892, 350.061039619, 1709434, 7.7e-05), alg_cluster.Cluster(set(['06019', '06039']), 95.8235848204, 288.669728653, 922516, 6.34662032962e-05), alg_cluster.Cluster(set(['06067', '06075', '06081', '06001', '06085', '06113', '06101']), 62.8105828117, 258.407213927, 6081309, 6.59259004928e-05), alg_cluster.Cluster(set(['06021', '06089']), 75.6645803941, 192.333495442, 189709, 5.86732785477e-05), alg_cluster.Cluster(set(['08005', '08001', '08031']), 376.551142131, 267.577115777, 1406460, 6.86979075125e-05), alg_cluster.Cluster(set(['09003']), 925.917212741, 177.152290276, 857183, 5.7e-05), alg_cluster.Cluster(set(['12073']), 762.463896365, 477.365342219, 239452, 6.1e-05), alg_cluster.Cluster(set(['13313', '47065']), 733.639126975, 371.72980828, 391421, 5.99330541795e-05), alg_cluster.Cluster(set(['13135', '13067', '13247', '13151', '13121', '13089', '13063']), 752.643396816, 399.380600745, 3104039, 6.59099199462e-05), alg_cluster.Cluster(set(['13245']), 796.799727342, 404.391349655, 199775, 5.9e-05), alg_cluster.Cluster(set(['19163']), 621.490118929, 227.666851619, 158668, 5.6e-05), alg_cluster.Cluster(set(['17031']), 668.978975824, 219.400257219, 5376741, 6.1e-05), alg_cluster.Cluster(set(['21019']), 768.726553092, 290.270551648, 49752, 5.8e-05), alg_cluster.Cluster(set(['21111']), 715.347723878, 301.167740487, 693604, 5.9e-05), alg_cluster.Cluster(set(['22017']), 570.826412839, 442.202574191, 252161, 6.2e-05), alg_cluster.Cluster(set(['22071']), 651.338581076, 496.465402252, 484674, 6.4e-05), alg_cluster.Cluster(set(['25025', '25017']), 945.61207339, 156.985293113, 2155203, 6.04809226787e-05), alg_cluster.Cluster(set(['26163', '26125']), 745.1476224, 197.473835078, 3255318, 6.14321734466e-05), alg_cluster.Cluster(set(['27123', '27053']), 572.136841573, 151.345524697, 1627235, 5.73718977284e-05), alg_cluster.Cluster(set(['29189', '29510']), 629.976164517, 297.473005985, 1364504, 6.22965861588e-05), alg_cluster.Cluster(set(['28027']), 631.700027283, 400.68741948, 30622, 6e-05), alg_cluster.Cluster(set(['28159']), 663.514261498, 425.274137823, 20160, 5.9e-05), alg_cluster.Cluster(set(['28049']), 638.051593606, 445.785870317, 250800, 6e-05), alg_cluster.Cluster(set(['37119']), 813.724315147, 356.853362811, 695454, 5.6e-05), alg_cluster.Cluster(set(['31109', '31055']), 522.63784996, 242.365927507, 713876, 6.1649391491e-05), alg_cluster.Cluster(set(['36119', '36005', '34003', '34013', '34017', '36085', '34023', '34031', '36061', '36081', '36103', '36047', '36059', '34039']), 912.582872765, 205.741362248, 15734128, 8.80317462143e-05), alg_cluster.Cluster(set(['34007', '42101']), 895.817161022, 228.943706724, 2026482, 5.77488593533e-05), alg_cluster.Cluster(set(['39035']), 776.351457758, 216.558042612, 1393978, 5.8e-05), alg_cluster.Cluster(set(['53011', '41051', '41067', '41005']), 100.699663547, 79.3107064609, 1789457, 7.73218926188e-05), alg_cluster.Cluster(set(['42003', '54009']), 808.812984502, 234.02138583, 1307113, 6.13114895193e-05), alg_cluster.Cluster(set(['47037']), 700.009323976, 350.107265446, 569891, 6.1e-05), alg_cluster.Cluster(set(['47093']), 753.012743594, 348.235180569, 382032, 5.6e-05), alg_cluster.Cluster(set(['48201', '48245']), 542.286222705, 504.62385661, 3652629, 5.97929839028e-05), alg_cluster.Cluster(set(['51520']), 784.05333332, 328.847863787, 17367, 5.6e-05), alg_cluster.Cluster(set(['11001', '24033', '24005', '24031', '51013', '51059', '24510', '51510', '51840', '24027', '51610']), 867.561803011, 256.631780926, 5221650, 6.55267515058e-05), alg_cluster.Cluster(set(['51775', '51680', '51770', '51820']), 827.430593192, 303.827886524, 204447, 6.12496294883e-05), alg_cluster.Cluster(set(['51087', '51570', '51760']), 866.047992388, 293.409901526, 476987, 7.2289332833e-05), alg_cluster.Cluster(set(['53033']), 125.27486023, 39.1497730391, 1737034, 5.8e-05), alg_cluster.Cluster(set(['55079']), 664.855000617, 192.484141264, 940164, 7.4e-05)])





#print slow_closest_pairs([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0), alg_cluster.Cluster(set([]), 4, 0, 1, 0), alg_cluster.Cluster(set([]), 5, 0, 1, 0), alg_cluster.Cluster(set([]), 6, 0, 1, 0), alg_cluster.Cluster(set([]), 7, 0, 1, 0), alg_cluster.Cluster(set([]), 8, 0, 1, 0), alg_cluster.Cluster(set([]), 9, 0, 1, 0), alg_cluster.Cluster(set([]), 10, 0, 1, 0), alg_cluster.Cluster(set([]), 11, 0, 1, 0), alg_cluster.Cluster(set([]), 12, 0, 1, 0), alg_cluster.Cluster(set([]), 13, 0, 1, 0), alg_cluster.Cluster(set([]), 14, 0, 1, 0), alg_cluster.Cluster(set([]), 15, 0, 1, 0), alg_cluster.Cluster(set([]), 16, 0, 1, 0), alg_cluster.Cluster(set([]), 17, 0, 1, 0), alg_cluster.Cluster(set([]), 18, 0, 1, 0), alg_cluster.Cluster(set([]), 19, 0, 1, 0)])

#fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0), alg_cluster.Cluster(set([]), 4, 0, 1, 0), alg_cluster.Cluster(set([]), 5, 0, 1, 0), alg_cluster.Cluster(set([]), 6, 0, 1, 0), alg_cluster.Cluster(set([]), 7, 0, 1, 0), alg_cluster.Cluster(set([]), 8, 0, 1, 0), alg_cluster.Cluster(set([]), 9, 0, 1, 0), alg_cluster.Cluster(set([]), 10, 0, 1, 0), alg_cluster.Cluster(set([]), 11, 0, 1, 0), alg_cluster.Cluster(set([]), 12, 0, 1, 0), alg_cluster.Cluster(set([]), 13, 0, 1, 0), alg_cluster.Cluster(set([]), 14, 0, 1, 0), alg_cluster.Cluster(set([]), 15, 0, 1, 0), alg_cluster.Cluster(set([]), 16, 0, 1, 0), alg_cluster.Cluster(set([]), 17, 0, 1, 0), alg_cluster.Cluster(set([]), 18, 0, 1, 0), alg_cluster.Cluster(set([]), 19, 0, 1, 0)])
#1
#print fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0)])

#cProfile.run('fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0), alg_cluster.Cluster(set([]), 4, 0, 1, 0), alg_cluster.Cluster(set([]), 5, 0, 1, 0), alg_cluster.Cluster(set([]), 6, 0, 1, 0), alg_cluster.Cluster(set([]), 7, 0, 1, 0), alg_cluster.Cluster(set([]), 8, 0, 1, 0), alg_cluster.Cluster(set([]), 9, 0, 1, 0), alg_cluster.Cluster(set([]), 10, 0, 1, 0), alg_cluster.Cluster(set([]), 11, 0, 1, 0), alg_cluster.Cluster(set([]), 12, 0, 1, 0), alg_cluster.Cluster(set([]), 13, 0, 1, 0), alg_cluster.Cluster(set([]), 14, 0, 1, 0), alg_cluster.Cluster(set([]), 15, 0, 1, 0), alg_cluster.Cluster(set([]), 16, 0, 1, 0), alg_cluster.Cluster(set([]), 17, 0, 1, 0), alg_cluster.Cluster(set([]), 18, 0, 1, 0), alg_cluster.Cluster(set([]), 19, 0, 1, 0)])')

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    return []



    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    # initialize k-means clusters to be initial clusters with largest populations

    return []


#cProfile.run("fast_closest_pair([alg_cluster.Cluster(set(['01101']), 720.281573781, 440.436162917, 223510, 5.7e-05), alg_cluster.Cluster(set(['01121']), 718.485365885, 413.521338651, 80321, 4.9e-05), alg_cluster.Cluster(set(['01117']), 709.193528999, 417.394467797, 143293, 5.6e-05), alg_cluster.Cluster(set(['01125']), 692.900099393, 417.773844647, 164875, 5.4e-05), alg_cluster.Cluster(set(['01073']), 704.191210749, 411.014665198, 662047, 7.3e-05), alg_cluster.Cluster(set(['01115']), 714.563978269, 406.272136377, 64742, 4.7e-05), alg_cluster.Cluster(set(['01015']), 723.907941153, 403.837487318, 112249, 5.6e-05), alg_cluster.Cluster(set(['01055']), 719.112287909, 398.290991634, 103459, 4.9e-05), alg_cluster.Cluster(set(['01103']), 702.624988295, 389.788894045, 111064, 5.3e-05), alg_cluster.Cluster(set(['01033']), 684.091279484, 385.661834299, 54984, 4.6e-05), alg_cluster.Cluster(set(['01077']), 686.294590746, 380.947137668, 87966, 4.6e-05), alg_cluster.Cluster(set(['01089']), 707.938558006, 382.483904975, 276700, 5.1e-05), alg_cluster.Cluster(set(['01081']), 736.280761314, 430.281309969, 115092, 5e-05), alg_cluster.Cluster(set(['01113']), 740.385154867, 436.939588695, 49756, 5.6e-05), alg_cluster.Cluster(set(['05119']), 598.676543754, 389.524749021, 361474, 5.3e-05), alg_cluster.Cluster(set(['05139']), 595.14987863, 427.226433206, 45629, 5.4e-05), alg_cluster.Cluster(set(['04013']), 214.128077618, 396.893960776, 3072149, 6.8e-05), alg_cluster.Cluster(set(['06025']), 156.397958859, 393.161127277, 142361, 5.6e-05), alg_cluster.Cluster(set(['06065']), 146.410389633, 374.21707964, 1545387, 6.1e-05), alg_cluster.Cluster(set(['06073']), 129.2075529, 387.064888184, 2813833, 6.6e-05), alg_cluster.Cluster(set(['06059']), 113.997715586, 368.503452566, 2846289, 9.8e-05), alg_cluster.Cluster(set(['06037']), 105.369854549, 359.050126004, 9519338, 0.00011), alg_cluster.Cluster(set(['06111']), 93.4973310868, 344.590570899, 753197, 5.8e-05), alg_cluster.Cluster(set(['06083']), 76.0382837186, 340.420376302, 399347, 6.4e-05), alg_cluster.Cluster(set(['06029']), 103.787886113, 326.006585349, 661645, 9.7e-05), alg_cluster.Cluster(set(['06071']), 148.402461892, 350.061039619, 1709434, 7.7e-05), alg_cluster.Cluster(set(['06027']), 136.048381588, 306.102582286, 17945, 5.3e-05), alg_cluster.Cluster(set(['06107']), 108.085024898, 306.351832438, 368021, 5.8e-05), alg_cluster.Cluster(set(['06031']), 89.2713893096, 304.772281089, 129461, 5.1e-05), alg_cluster.Cluster(set(['06039']), 97.2145136451, 278.975077449, 123109, 6e-05), alg_cluster.Cluster(set(['06019']), 95.6093812211, 290.162708843, 799407, 6.4e-05), alg_cluster.Cluster(set(['06047']), 80.1217093401, 275.749681794, 210554, 4.7e-05), alg_cluster.Cluster(set(['06081']), 52.6171444847, 262.707477827, 707161, 5.6e-05), alg_cluster.Cluster(set(['06001']), 61.782098866, 259.312457296, 1443741, 7e-05), alg_cluster.Cluster(set(['06085']), 63.1509653633, 270.516712105, 1682585, 6.3e-05), alg_cluster.Cluster(set(['06099']), 77.5948233373, 265.302047042, 446997, 5.1e-05), alg_cluster.Cluster(set(['06077']), 74.1740312349, 256.485831492, 563598, 5.2e-05), alg_cluster.Cluster(set(['06013']), 62.7064814493, 253.075658488, 948816, 5e-05), alg_cluster.Cluster(set(['06067']), 74.3547338322, 245.49501455, 1223499, 6.1e-05), alg_cluster.Cluster(set(['06095']), 64.1452346104, 245.330036641, 394542, 4.6e-05), alg_cluster.Cluster(set(['06075']), 52.7404001225, 254.517429395, 776733, 8.4e-05), alg_cluster.Cluster(set(['06113']), 68.2602083189, 236.862609218, 168660, 5.9e-05), alg_cluster.Cluster(set(['06061']), 90.0298511972, 233.575536165, 248399, 5.2e-05), alg_cluster.Cluster(set(['06115']), 81.8982358215, 225.444950413, 60219, 4.9e-05), alg_cluster.Cluster(set(['06101']), 74.2003718491, 229.646592975, 78930, 5.6e-05), alg_cluster.Cluster(set(['06007']), 79.7767444918, 214.910128237, 203171, 4.7e-05), alg_cluster.Cluster(set(['06021']), 65.2043358182, 213.245337355, 26453, 6.9e-05), alg_cluster.Cluster(set(['06089']), 77.359494209, 188.945068958, 163256, 5.7e-05), alg_cluster.Cluster(set(['08005']), 380.281283151, 270.268826873, 487967, 5.9e-05), alg_cluster.Cluster(set(['08001']), 379.950978294, 265.078784954, 363857, 6.6e-05), alg_cluster.Cluster(set(['08031']), 371.038986573, 266.847932979, 554636, 7.9e-05), alg_cluster.Cluster(set(['08059']), 364.301409054, 270.903209636, 527056, 5.5e-05), alg_cluster.Cluster(set(['09003']), 925.917212741, 177.152290276, 857183, 5.7e-05), alg_cluster.Cluster(set(['09005']), 917.693447363, 179.72354771, 182193, 4.8e-05), alg_cluster.Cluster(set(['09001']), 917.147792831, 191.892113077, 882567, 5.3e-05), alg_cluster.Cluster(set(['09009']), 924.915452791, 187.557375239, 824008, 5.4e-05), alg_cluster.Cluster(set(['09007']), 931.146412937, 184.643328414, 155071, 5.1e-05), alg_cluster.Cluster(set(['09013']), 932.609837236, 174.394154191, 136364, 5e-05), alg_cluster.Cluster(set(['10003']), 888.26796027, 239.785084878, 500265, 4.9e-05), alg_cluster.Cluster(set(['12071']), 822.736368501, 559.319167615, 440888, 4.7e-05), alg_cluster.Cluster(set(['12086']), 855.717845944, 576.450702277, 2253362, 4.9e-05), alg_cluster.Cluster(set(['12011']), 854.318125011, 564.174521982, 1623018, 5e-05), alg_cluster.Cluster(set(['12099']), 852.886370359, 552.951546188, 1131184, 5.1e-05), alg_cluster.Cluster(set(['12057']), 810.083518173, 529.957501469, 998948, 4.7e-05), alg_cluster.Cluster(set(['12095']), 828.477422871, 512.999289781, 896344, 5.2e-05), alg_cluster.Cluster(set(['12117']), 829.684398031, 508.399477043, 365196, 4.9e-05), alg_cluster.Cluster(set(['12019']), 812.760924762, 481.531359294, 140814, 4.6e-05), alg_cluster.Cluster(set(['12073']), 762.463896365, 477.365342219, 239452, 6.1e-05), alg_cluster.Cluster(set(['12065']), 770.707334208, 476.851119419, 12902, 4.7e-05), alg_cluster.Cluster(set(['12023']), 796.544243535, 477.588016437, 56513, 5e-05), alg_cluster.Cluster(set(['12031']), 815.145119735, 473.114295395, 778879, 4.9e-05), alg_cluster.Cluster(set(['13087']), 755.693541123, 468.194002931, 28240, 4.9e-05), alg_cluster.Cluster(set(['13275']), 768.884153625, 466.608446685, 42737, 5.5e-05), alg_cluster.Cluster(set(['13095']), 761.086378978, 451.967184234, 96065, 4.9e-05), alg_cluster.Cluster(set(['13115']), 734.580792996, 390.450110664, 90565, 5.2e-05), alg_cluster.Cluster(set(['13313']), 737.308367745, 378.040993858, 83525, 5.6e-05), alg_cluster.Cluster(set(['13047']), 734.388362226, 375.991769202, 53282, 5e-05), alg_cluster.Cluster(set(['13295']), 731.703883397, 380.217410319, 61053, 5.4e-05), alg_cluster.Cluster(set(['13215']), 745.265661102, 430.987078939, 186291, 5.9e-05), alg_cluster.Cluster(set(['13285']), 741.206792819, 419.291408746, 58779, 4.7e-05), alg_cluster.Cluster(set(['13045']), 738.792024777, 406.300529008, 87268, 4.6e-05), alg_cluster.Cluster(set(['13223']), 741.778484027, 398.177004976, 81678, 4.8e-05), alg_cluster.Cluster(set(['13129']), 740.472181415, 384.60635928, 44104, 5e-05), alg_cluster.Cluster(set(['13015']), 741.560012096, 390.864452051, 76019, 4.8e-05), alg_cluster.Cluster(set(['13067']), 747.238620236, 397.293799252, 607751, 6.4e-05), alg_cluster.Cluster(set(['13097']), 744.596506113, 402.962208469, 92174, 5.3e-05), alg_cluster.Cluster(set(['13077']), 745.613117606, 411.392480996, 89215, 4.7e-05), alg_cluster.Cluster(set(['13153']), 768.866056624, 429.26170891, 110765, 4.6e-05), alg_cluster.Cluster(set(['13021']), 767.744846588, 421.175433164, 153887, 5.4e-05), alg_cluster.Cluster(set(['13255']), 754.429031747, 412.402694941, 58417, 4.9e-05), alg_cluster.Cluster(set(['13113']), 750.29432181, 409.288659145, 91263, 5.1e-05), alg_cluster.Cluster(set(['13063']), 752.853876848, 406.722877803, 236517, 6.6e-05), alg_cluster.Cluster(set(['13151']), 756.589546538, 407.288873768, 119341, 5.6e-05), alg_cluster.Cluster(set(['13089']), 754.465443436, 400.059456026, 665865, 6.8e-05), alg_cluster.Cluster(set(['13121']), 750.160287596, 399.907752014, 816006, 7e-05), alg_cluster.Cluster(set(['13057']), 748.412720226, 389.846908157, 141903, 5.3e-05), alg_cluster.Cluster(set(['13117']), 755.145102581, 389.478397813, 98407, 5.1e-05), alg_cluster.Cluster(set(['13135']), 758.038826857, 395.110327675, 588448, 6.3e-05), alg_cluster.Cluster(set(['13247']), 758.37864157, 402.49780372, 70111, 5.6e-05), alg_cluster.Cluster(set(['13217']), 762.124521207, 404.381839078, 62001, 5.2e-05), alg_cluster.Cluster(set(['13297']), 763.860443745, 398.939532724, 60687, 5e-05), alg_cluster.Cluster(set(['13013']), 763.778282645, 393.625933437, 46144, 4.7e-05), alg_cluster.Cluster(set(['13059']), 770.365599785, 394.047543369, 101489, 5.3e-05), alg_cluster.Cluster(set(['13219']), 769.191246041, 396.756414858, 26225, 4.7e-05), alg_cluster.Cluster(set(['13245']), 796.799727342, 404.391349655, 199775, 5.9e-05), alg_cluster.Cluster(set(['13073']), 792.804322285, 400.662049665, 89288, 5e-05), alg_cluster.Cluster(set(['19163']), 621.490118929, 227.666851619, 158668, 5.6e-05), alg_cluster.Cluster(set(['19153']), 570.801738263, 228.668095362, 374601, 5.2e-05), alg_cluster.Cluster(set(['19013']), 591.836020306, 209.588448378, 128012, 4.6e-05), alg_cluster.Cluster(set(['19057']), 612.882010424, 244.949915243, 42351, 5.1e-05), alg_cluster.Cluster(set(['17161']), 623.059973539, 231.112598464, 149374, 5e-05), alg_cluster.Cluster(set(['17043']), 664.97964782, 219.666485923, 904161, 5.1e-05), alg_cluster.Cluster(set(['17031']), 668.978975824, 219.400257219, 5376741, 6.1e-05), alg_cluster.Cluster(set(['17201']), 645.722085, 209.852492823, 278418, 4.8e-05), alg_cluster.Cluster(set(['18089']), 677.840033419, 228.268571284, 484564, 4.8e-05), alg_cluster.Cluster(set(['18097']), 703.47637833, 264.614798668, 860454, 4.8e-05), alg_cluster.Cluster(set(['20173']), 502.059178492, 322.563937328, 452869, 5.1e-05), alg_cluster.Cluster(set(['20091']), 549.942556013, 294.526691953, 451086, 5e-05), alg_cluster.Cluster(set(['20209']), 550.661615218, 289.397706643, 157882, 5.1e-05), alg_cluster.Cluster(set(['21019']), 768.726553092, 290.270551648, 49752, 5.8e-05), alg_cluster.Cluster(set(['21067']), 738.000675961, 302.005037855, 260512, 4.8e-05), alg_cluster.Cluster(set(['21117']), 734.066615163, 281.167681124, 151464, 5e-05), alg_cluster.Cluster(set(['21111']), 715.347723878, 301.167740487, 693604, 5.9e-05), alg_cluster.Cluster(set(['22015']), 575.844790614, 439.774115304, 98310, 4.9e-05), alg_cluster.Cluster(set(['22017']), 570.826412839, 442.202574191, 252161, 6.2e-05), alg_cluster.Cluster(set(['22121']), 622.795050771, 488.85623181, 21601, 5.2e-05), alg_cluster.Cluster(set(['22047']), 621.964681856, 493.299089267, 33320, 4.7e-05), alg_cluster.Cluster(set(['22033']), 627.532921181, 486.959525017, 412852, 5.3e-05), alg_cluster.Cluster(set(['22095']), 639.022908787, 496.564276607, 43044, 5.1e-05), alg_cluster.Cluster(set(['22071']), 651.338581076, 496.465402252, 484674, 6.4e-05), alg_cluster.Cluster(set(['22051']), 647.254240096, 504.485538044, 455466, 4.6e-05), alg_cluster.Cluster(set(['25017']), 943.405755498, 156.504310828, 1465396, 5.6e-05), alg_cluster.Cluster(set(['25025']), 950.299079197, 158.007070966, 689807, 7e-05), alg_cluster.Cluster(set(['25021']), 948.811505542, 162.842169307, 650308, 5.3e-05), alg_cluster.Cluster(set(['25013']), 925.818389384, 169.274417202, 456228, 5.2e-05), alg_cluster.Cluster(set(['25015']), 923.51496257, 165.065795331, 152251, 4.6e-05), alg_cluster.Cluster(set(['24001']), 834.528507681, 249.862506444, 74930, 4.8e-05), alg_cluster.Cluster(set(['24043']), 849.08430905, 247.089766046, 131923, 4.6e-05), alg_cluster.Cluster(set(['24510']), 872.946822486, 249.834427518, 651154, 7.4e-05), alg_cluster.Cluster(set(['24033']), 870.786325575, 261.829970016, 801515, 6.4e-05), alg_cluster.Cluster(set(['24003']), 874.299504257, 257.092978322, 489656, 5.3e-05), alg_cluster.Cluster(set(['24027']), 867.127763298, 252.141340019, 247842, 6e-05), alg_cluster.Cluster(set(['24031']), 863.180208628, 255.65657011, 873341, 6.5e-05), alg_cluster.Cluster(set(['24025']), 876.595690503, 242.900377968, 218590, 4.6e-05), alg_cluster.Cluster(set(['24005']), 871.921241442, 246.932531615, 754292, 6.1e-05), alg_cluster.Cluster(set(['24021']), 858.130790832, 248.37974611, 195277, 5e-05), alg_cluster.Cluster(set(['26163']), 746.37046732, 200.570021537, 2061162, 6.4e-05), alg_cluster.Cluster(set(['26125']), 743.036942153, 192.129690868, 1194156, 5.7e-05), alg_cluster.Cluster(set(['26099']), 750.610280372, 190.468671453, 788149, 5.1e-05), alg_cluster.Cluster(set(['27123']), 576.516685202, 151.219277482, 511035, 5.6e-05), alg_cluster.Cluster(set(['27003']), 573.942484199, 145.118314377, 298084, 4.6e-05), alg_cluster.Cluster(set(['27053']), 570.131597541, 151.403325043, 1116200, 5.8e-05), alg_cluster.Cluster(set(['29095']), 558.451289477, 291.559180265, 654880, 4.6e-05), alg_cluster.Cluster(set(['29510']), 632.327321169, 297.184524592, 348189, 6.9e-05), alg_cluster.Cluster(set(['29183']), 625.995955203, 293.938397646, 283883, 4.7e-05), alg_cluster.Cluster(set(['29189']), 629.170659449, 297.571839563, 1016315, 6e-05), alg_cluster.Cluster(set(['28043']), 647.649972548, 410.394464547, 23263, 4.7e-05), alg_cluster.Cluster(set(['28087']), 674.418402473, 415.122758999, 61586, 4.6e-05), alg_cluster.Cluster(set(['28033']), 642.267628251, 384.839249499, 107199, 4.6e-05), alg_cluster.Cluster(set(['28027']), 631.700027283, 400.68741948, 30622, 6e-05), alg_cluster.Cluster(set(['28159']), 663.514261498, 425.274137823, 20160, 5.9e-05), alg_cluster.Cluster(set(['28089']), 644.644674143, 437.339606833, 74674, 4.6e-05), alg_cluster.Cluster(set(['28121']), 647.272159578, 445.553667274, 115327, 4.8e-05), alg_cluster.Cluster(set(['28049']), 638.051593606, 445.785870317, 250800, 6e-05), alg_cluster.Cluster(set(['28075']), 672.167227537, 440.608524349, 78161, 4.6e-05), alg_cluster.Cluster(set(['28035']), 662.340841725, 469.562070989, 72604, 5e-05), alg_cluster.Cluster(set(['37071']), 806.573724958, 356.877472978, 190365, 4.8e-05), alg_cluster.Cluster(set(['37119']), 813.724315147, 356.853362811, 695454, 5.6e-05), alg_cluster.Cluster(set(['37057']), 823.18698731, 342.886324895, 147246, 4.6e-05), alg_cluster.Cluster(set(['37025']), 818.35071393, 352.864665547, 131063, 4.7e-05), alg_cluster.Cluster(set(['37081']), 829.726844142, 334.637483646, 421048, 4.8e-05), alg_cluster.Cluster(set(['31153']), 527.065884457, 242.564882077, 122595, 4.9e-05), alg_cluster.Cluster(set(['31055']), 525.799353573, 238.14275337, 463585, 6.2e-05), alg_cluster.Cluster(set(['31109']), 516.78216337, 250.188023316, 250291, 6.1e-05), alg_cluster.Cluster(set(['33011']), 936.826960243, 147.991772374, 380841, 5e-05), alg_cluster.Cluster(set(['36085']), 908.749199508, 211.307161341, 443728, 7e-05), alg_cluster.Cluster(set(['34013']), 906.236730753, 206.977429459, 793633, 7.1e-05), alg_cluster.Cluster(set(['34039']), 905.587082153, 210.045085725, 522541, 7.3e-05), alg_cluster.Cluster(set(['34017']), 909.08042421, 207.462937763, 608975, 9.1e-05), alg_cluster.Cluster(set(['34003']), 907.896066895, 202.302470427, 884118, 6.9e-05), alg_cluster.Cluster(set(['34023']), 904.976453741, 215.001458637, 750162, 5.9e-05), alg_cluster.Cluster(set(['34031']), 904.161746346, 201.712206531, 489049, 6.3e-05), alg_cluster.Cluster(set(['34021']), 900.837767215, 220.161475984, 350761, 4.6e-05), alg_cluster.Cluster(set(['34007']), 899.061431482, 232.054232622, 508932, 5.7e-05), alg_cluster.Cluster(set(['34005']), 903.696809122, 229.406192432, 423394, 4.6e-05), alg_cluster.Cluster(set(['32003']), 178.153492162, 324.160586278, 1375765, 4.9e-05), alg_cluster.Cluster(set(['36001']), 900.893220363, 164.489226174, 294565, 4.9e-05), alg_cluster.Cluster(set(['36029']), 820.38582573, 177.013330392, 950265, 5e-05), alg_cluster.Cluster(set(['36061']), 911.072622034, 205.783086757, 1537195, 0.00015), alg_cluster.Cluster(set(['36005']), 912.315497328, 203.674106811, 1332650, 0.00011), alg_cluster.Cluster(set(['36047']), 911.595580089, 208.928374072, 2465326, 9.8e-05), alg_cluster.Cluster(set(['36087']), 907.86300402, 197.579715272, 286753, 4.9e-05), alg_cluster.Cluster(set(['36059']), 917.384980291, 205.43647538, 1334544, 7.6e-05), alg_cluster.Cluster(set(['36081']), 913.462051588, 207.615750359, 2229379, 8.9e-05), alg_cluster.Cluster(set(['36103']), 929.241649488, 199.278463003, 1419369, 6.3e-05), alg_cluster.Cluster(set(['36119']), 912.141547823, 196.592589736, 923459, 6.5e-05), alg_cluster.Cluster(set(['36079']), 910.914101605, 190.332224, 95745, 4.8e-05), alg_cluster.Cluster(set(['36083']), 907.985922231, 160.259081442, 152538, 4.7e-05), alg_cluster.Cluster(set(['39087']), 770.625409557, 283.93917465, 62319, 4.6e-05), alg_cluster.Cluster(set(['39061']), 733.263799261, 275.315430247, 845303, 5.4e-05), alg_cluster.Cluster(set(['39017']), 731.844357783, 269.494670001, 332807, 4.9e-05), alg_cluster.Cluster(set(['39049']), 758.062157993, 253.603273009, 1068978, 5.2e-05), alg_cluster.Cluster(set(['39035']), 776.351457758, 216.558042612, 1393978, 5.8e-05), alg_cluster.Cluster(set(['39095']), 742.473618138, 216.811437951, 455054, 4.6e-05), alg_cluster.Cluster(set(['40121']), 534.015957707, 386.972736212, 43953, 5.2e-05), alg_cluster.Cluster(set(['40143']), 529.254373189, 359.119882043, 563299, 5.1e-05), alg_cluster.Cluster(set(['41029']), 78.4141193387, 147.629027207, 181269, 5.1e-05), alg_cluster.Cluster(set(['41047']), 97.399304684, 93.4988892144, 284834, 4.8e-05), alg_cluster.Cluster(set(['41005']), 103.421444616, 88.318590492, 338391, 6.6e-05), alg_cluster.Cluster(set(['41051']), 103.293707198, 79.5194104381, 660486, 9.3e-05), alg_cluster.Cluster(set(['41067']), 92.2254623376, 76.2593957841, 445342, 7.3e-05), alg_cluster.Cluster(set(['42101']), 894.72914873, 227.900547575, 1517550, 5.8e-05), alg_cluster.Cluster(set(['42003']), 809.003419092, 233.899638663, 1281666, 6.1e-05), alg_cluster.Cluster(set(['42011']), 878.575486588, 221.678319842, 373638, 4.6e-05), alg_cluster.Cluster(set(['42045']), 890.848103047, 231.287395353, 550864, 5.2e-05), alg_cluster.Cluster(set(['45003']), 804.805415327, 398.777010123, 142552, 4.8e-05), alg_cluster.Cluster(set(['45063']), 810.799412401, 389.504491524, 216014, 4.8e-05), alg_cluster.Cluster(set(['45079']), 816.541641816, 385.156707247, 320677, 5.4e-05), alg_cluster.Cluster(set(['45007']), 782.226804679, 379.132979851, 165740, 4.6e-05), alg_cluster.Cluster(set(['45091']), 807.886971209, 364.469906345, 164614, 4.7e-05), alg_cluster.Cluster(set(['45083']), 793.239375577, 367.754402204, 253791, 4.8e-05), alg_cluster.Cluster(set(['45045']), 785.676714035, 369.542097768, 379616, 5.2e-05), alg_cluster.Cluster(set(['47163']), 782.499804827, 331.593361246, 153048, 4.7e-05), alg_cluster.Cluster(set(['47053']), 660.602484901, 357.318624524, 48152, 4.6e-05), alg_cluster.Cluster(set(['47157']), 643.395763039, 378.031744605, 897472, 5.5e-05), alg_cluster.Cluster(set(['47149']), 707.710145119, 356.803460768, 182023, 5e-05), alg_cluster.Cluster(set(['47037']), 700.009323976, 350.107265446, 569891, 6.1e-05), alg_cluster.Cluster(set(['47165']), 705.571676152, 342.569345394, 130449, 4.6e-05), alg_cluster.Cluster(set(['47065']), 732.643747577, 370.017730905, 307896, 6.1e-05), alg_cluster.Cluster(set(['47093']), 753.012743594, 348.235180569, 382032, 5.6e-05), alg_cluster.Cluster(set(['48003']), 398.962651077, 443.958242671, 13004, 5.3e-05), alg_cluster.Cluster(set(['48029']), 477.886663525, 514.095891984, 1392931, 5e-05), alg_cluster.Cluster(set(['48157']), 533.434165736, 513.008691943, 354452, 4.6e-05), alg_cluster.Cluster(set(['48201']), 540.54731652, 504.62993865, 3400578, 6e-05), alg_cluster.Cluster(set(['48245']), 565.746895809, 504.541799993, 252051, 5.7e-05), alg_cluster.Cluster(set(['48361']), 571.064681764, 498.867855628, 84966, 4.6e-05), alg_cluster.Cluster(set(['48453']), 493.032076052, 493.597339677, 812280, 5.2e-05), alg_cluster.Cluster(set(['48041']), 522.88823653, 487.351397054, 152415, 4.6e-05), alg_cluster.Cluster(set(['48439']), 503.673815634, 437.477028749, 1446219, 5e-05), alg_cluster.Cluster(set(['48113']), 513.657901701, 437.682966844, 2218899, 5.4e-05), alg_cluster.Cluster(set(['48365']), 562.161603376, 451.397747537, 22756, 4.8e-05), alg_cluster.Cluster(set(['48183']), 552.333188086, 444.322743975, 111379, 5.5e-05), alg_cluster.Cluster(set(['48423']), 542.731029941, 446.457985602, 174706, 4.7e-05), alg_cluster.Cluster(set(['48203']), 560.270010669, 442.325574621, 62110, 5e-05), alg_cluster.Cluster(set(['48085']), 517.70778434, 427.895646823, 491675, 4.8e-05), alg_cluster.Cluster(set(['51520']), 784.05333332, 328.847863787, 17367, 5.6e-05), alg_cluster.Cluster(set(['51640']), 806.823088186, 324.555032883, 6837, 5.2e-05), alg_cluster.Cluster(set(['51750']), 811.690750985, 312.898714856, 15859, 4.6e-05), alg_cluster.Cluster(set(['51610']), 864.078108667, 261.655667801, 10377, 6.9e-05), alg_cluster.Cluster(set(['51013']), 865.681962839, 261.222875114, 189453, 7.7e-05), alg_cluster.Cluster(set(['51775']), 820.111751617, 307.695502162, 24747, 5.8e-05), alg_cluster.Cluster(set(['51161']), 820.49953559, 307.816533009, 85778, 5.4e-05), alg_cluster.Cluster(set(['51690']), 826.020074281, 321.016553783, 15416, 4.9e-05), alg_cluster.Cluster(set(['51590']), 834.603738103, 321.684114822, 48411, 4.8e-05), alg_cluster.Cluster(set(['51680']), 835.264653899, 302.326633095, 65269, 5.8e-05), alg_cluster.Cluster(set(['51515']), 829.535165128, 304.77544828, 6299, 4.7e-05), alg_cluster.Cluster(set(['51770']), 821.912162221, 307.548990323, 94911, 6.5e-05), alg_cluster.Cluster(set(['51820']), 837.346467474, 285.851438947, 19520, 5.8e-05), alg_cluster.Cluster(set(['51540']), 845.239184424, 285.286609195, 45049, 5.4e-05)])")
