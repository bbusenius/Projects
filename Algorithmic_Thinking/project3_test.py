import alg_project3_template as project3
import alg_cluster
import csv
import random

for run_counter in range(99):
    random.seed(run_counter)
    probability = random.randrange(10,100) / 100.0
    print "Run: ", run_counter, "p:", probability
    csv_file = open('unifiedCancerData_111.csv', 'r')
    reader = csv.reader(csv_file)
    cluster_list = []
    for row in reader:
        if random.random() > probability:
            continue
        new_cluster = alg_cluster.Cluster(
                int(row[0]),
                float(row[1]), float(row[2]),
                int(row[3]), float(row[4]))
        cluster_list.append(new_cluster)

    slow_res = project3.slow_closest_pairs(cluster_list)
    fast_res = project3.fast_closest_pair(cluster_list)

    print slow_res
    print fast_res

    assert fast_res in slow_res
