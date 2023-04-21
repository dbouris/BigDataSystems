#!/usr/bin/env python

"""
The combiner.py: Performs the calculations of the Combine Phase.

Takes as input the output of the mapper.
The combiner calculates foreach cluster the sum of the x and y coordinates of the points which have been assigned 
to it. As the job will be distributed to multiple clusters each combiner job calculates the partial sums. The number
of points contributed to the sum is also captured.
The output will be in tis format: "num_cluster ([subsum_x, subsum_y], num_points_participated)"
The output of the combiner is used as an input to the reducer which aggregates the partial sums.
"""

import sys
import ast

# variable to identify the cluster we are working on
working_cluster = None
# the cluster the line belongs
cluster = None
subsum = []

def parse_input(line):

    """ The function decodes the stdin which comes from the mapper """
    cluster, point = line.strip().split('\t', 1)
    point = ast.literal_eval(point)
    return cluster,point

# iterate over each line of the stdin
for line in sys.stdin:

    # decode the input and get the cluster and the coordinates of the point
    cluster, point = parse_input(line)

    # Note: The input is sorted by the clusterid so all the cluster 1 items will come first,
    # then the ones with cluster 2 and lastly the ones in the 3rd cluster
    # we use the cluster and current cluster to identify when one cluster is done and the 
    # other cluster starts (cluster != current cluster)
    
    # if we still have data about the current cluster, alter the sums
    if working_cluster == cluster:
        # add the x and y coordinates to the equivalent sums
        subsum[0] += point[0]
        subsum[1] += point[1]
        num_points += 1
     # if a new cluster starts, print the partial sum and the number of points participated in it
    else:
        if working_cluster:
            # Write cluster, partial sum and number
            print ('%s\t%s' % (working_cluster,
                (subsum, num_points)))
        
        # Update the sums with the values of the point of the new cluster
        subsum = point
        num_points = 1
        working_cluster = cluster

# output the sum and num of points of the last cluster as it does not happen above
if working_cluster == cluster:
    print ('%s\t%s' % (working_cluster, (subsum, num_points)))