#!/usr/bin/env python

"""
reducer.py: Performs the calculations of the Reduce Phase.

The reducer takes as input the output of the Combiner from the stdout 
This pahse aggregates the subsums of the x and y coordinates and calculates the average
respectively foreach cluster. The average of the x and y coordinates calculated foreach cluster
are the new centers.
"""

import sys
import ast

def parse_input(line):

    """This function decodes the input line from stdin"""

    cluster, partial = line.strip().split('\t', 1)
    sub_sum = ",".join(partial.split(",", 2)[:2]).replace("(", "")
    num_points = partial.split(",", 2)[2].replace(")", "")
    num_points = int(num_points)
    sub_sum = ast.literal_eval(sub_sum)
    return cluster, sub_sum, num_points

def calculate_center(total_sub_sum, num_points):

    """This function decodes the input line from stdin"""
    
    # the new centroid is calculated as the mean value of the x and y coordinates
    # of the points which have been assigned to the cluster
    xCenter = round(total_sub_sum[0] / num_points, 1)
    yCenter = round(total_sub_sum[1] / num_points, 1)
    # the new centroid is returned as a list in the std out
    new_centroid = [xCenter, yCenter]
    print('%s\t' % (new_centroid))

# instantiate some counters
working_cluster = None
total_sub_sum = []
cluster = None
num_points = 0


# iterate over all the input lines
for line in sys.stdin:

    # decode the line and get the clusterid, sub_sum and number of points that the sum is for
    cluster, sub_sum, num_points = parse_input(line)

    # Note: The input is sorted by the clusterid so all the cluster 1 items will come first,
    # then the ones with cluster 2 and lastly the ones in the 3rd cluster
    # we use the cluster and current cluster to identify when one cluster is done and the 
    # other cluster starts (cluster != current cluster)

    # if we still have data about the current cluster, alter the sums
    if working_cluster == cluster:
        total_sub_sum[0] += sub_sum[0]
        total_sub_sum[1] += sub_sum[1]
        num_points += num_points
    # if a new cluster starts, get the new centroid of the ready cluster
    else:
        # if the current cluster has a value, meaning that it is not the first iteration
        if working_cluster:
            calculate_center(total_sub_sum, num_points)
        # restart the sum variables to the first values of the new cluster
        total_sub_sum = sub_sum
        num_points = num_points
        working_cluster = cluster

# calculate the new center of the last cluster as it does not happen above
if working_cluster == cluster:
    calculate_center(total_sub_sum, num_points)
