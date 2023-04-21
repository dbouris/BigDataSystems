#!/usr/bin/env python

"""
The mapper.py: Performs the calculations of the Map Phase.

Takes as input all the points and their coordinates (x,y).
Based on the current centers this step calculates the closest center 
foreach point and assigns it to the equivalent cluster.
The returned values in the stdout are in the format: "num_cluster    [x,y]"
"""

import sys 
import numpy as np

def read_centers(centers_file):
    """Reads the centers from a CSV file."""
    with open(centers_file, "r") as f:
        centers = []
        # the old-centers file contains previous centers 
        # each center is represented with the x and y coordinates
        # each line represents one center
        for line in f:
            # decode the x and y coordinates into 2 separate variables
            x, y = map(float, line.strip().split(","))
            centers.append([x, y])
        return centers

def calculate_distances(point, centers):
    """Calculates the Manhattan distance between a point and each center."""
    distances = []
    for center in centers:
        # calculate the Manhattan distance between the point and the center
        x_distance = abs(point[0] - center[0])
        y_distance = abs(point[1] - center[1])
        distance = x_distance + y_distance
        # save all the distances in a list
        distances.append(distance)
    return distances

def find_closest_center(distances):
    """Finds the index of the closest center."""
    # find the closest center from the distances matrix 
    # the arg min function returns the index of the list -> the id of the center
    return np.argmin(distances)

centers = read_centers("files/current_centers.csv")

# iterate over each input line
for line in sys.stdin:
    # decode the line
    point = list(map(float, line.strip().split(",")))

    # get the diastance the point has fron each center
    distances = calculate_distances(point, centers)

    # find the closest center
    cluster = find_closest_center(distances)

    # print the result to std out 
    print('%s\t%s' % (cluster, point))