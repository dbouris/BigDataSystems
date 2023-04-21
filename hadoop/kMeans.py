#!/usr/bin/env python

"""
kMeans.py: Implements the K-Means algorithm using the Map - Combine - Reduce Hadoop Operation
"""

import ast
import random
import subprocess

# set a random seed for reproductivity
random.seed(13)

def emptyFiles():
    files = [current_centers, allCenters]
    for file in files:
        with open(file, 'w') as file:
            file.write('')

def getPoints(file):
    """ Gets all the x and y coordinates of the points from the file specified """
    with open(file, "r") as data:
        data = data.readlines()
        dataList = []
        for d in data:
            d = d.strip().split(",")
            d = [float(d[0]), float(d[1])]
            dataList.append(d)
    return dataList

def storeCenters(centers):
    """ Saves each group of calculated centers in a file """
    with open(allCenters, "a") as file:
        # iterate over all the centers and write them in the file
        for center in centers:
            file.write("%s\n" % str([center]).strip('[]'))

def getCenters(file_path):
    """ Gets the centers from the file specified. Each center is stored as a tuple of the 
    x and y coordinates and each line represents a center.
    """
    with open(file_path, "r") as cfile:
        # read all the lines of the centers file
        cfile = cfile.readlines()
        centers_all = []
        # iterate over all the lines - centers and append them in a list
        for center in cfile:
            center = ast.literal_eval(center)
            centers_all.append(center)
    return centers_all

def checkConvergence(previous_centers, new_centers):
    """ Checks if the current and previous centers have converged meaning that they have not changed 
    much between the two iterations of the algorithm. Takes as an input the two lists of the old and new centers """
    converged = False
    # sort them before as they might be in a different order
    # if they are the same, return True and stop the iterations
    if sorted(previous_centers) == sorted(new_centers):
        converged = True
    # else return False meaning that we need at least one more iteration
    return converged

def replaceOldCenters(centers):
    """ Replaces the old center with the newly calculated ones """
    # open the file with the w+ parameter which opens the file for writing and truncates the file to zero length.
    with open(current_centers, "w+") as file:
        # iterate over each center and write it to the file
        for center in centers:
            file.write("%s\n" % str([center]).strip('[]'))

if __name__ == "__main__":

    # specify the path foreach file used 
    current_centers = "files/current_centers.csv"
    dataPoints = "files/data-points.csv"
    LocalHadoopOutput = "files/LocalHadoopOutput/part-00000"
    allCenters = "files/all-centers.csv"


    emptyFiles()

    # Retrieve the initial data points
    dataPointsList = getPoints(dataPoints)
    # Randomly generate the initial centers foreach cluster
    num_clusters = 3 
    initialCentroids = random.sample(dataPointsList, k=num_clusters)
    replaceOldCenters(initialCentroids)
    storeCenters(initialCentroids)

    converged = False
    # As long as the centers have not converged, repeat 
    while (converged == False):
        
        # Connect with HDFS and run Map-Combine-Reduce process through the Hadoop Streaming
        # we need to specify the mapper - combiner and reducer files and also all the input files 
        # as well as the hadoop path where the output will be stored
        # the process below implements the first iteration of the KMeans algorithm

        map_combine_reduce = subprocess.run(["/Users/dimitrisbouris/hadoop-3.2.3/bin/hadoop", "jar",
        "/Users/dimitrisbouris/hadoop-3.2.3/share/hadoop/tools/lib/hadoop-streaming-3.2.3.jar",
        "-file", "mapper.py", "-mapper","mapper.py", "-file","combiner.py" ,"-combiner" ,"combiner.py",  
        "-file", "reducer.py", "-reducer", "reducer.py", "-file", "files/current_centers.csv", "-input", "/kmeans/data-points.csv",
        "-output","kmeans_output/output"], stdout=subprocess.PIPE)

        # After the completion of the first iteration, we will copy the output file from hdfs to the local folder
        # This output file will be used as input to the second iteration. This process will repeat foreach iteration of the algo.
        # The output file is stored in hadoop by default with the name "part-00000"
        # This file is the output of the reducer and thus represents the new centers

        copy = subprocess.run(["/Users/dimitrisbouris/hadoop-3.2.3/bin/hadoop", "fs", "-get", 
        "/user/dimitrisbouris/kmeans_output/output/part-00000", "files/LocalHadoopOutput/"])

        # delete the output directory created before as the hdfs throws an error as it attempts to recreate it
        delete = subprocess.run(["hdfs", "dfs", "-rm", "-r" , "/user/"])

        # get the old and new centers 
        previous_centers = getCenters(current_centers)
        new_centers = getCenters(LocalHadoopOutput)
        previous_centers= [list(center) for center in previous_centers]
        storeCenters(new_centers)

        # chech if they have converged 
        converged = checkConvergence(previous_centers, new_centers)
        # If the centers have changed run another iteration of the KMeans algo
        if converged == False:
            # Update the current centers file with the new ones
            replaceOldCenters(new_centers)
            # we also remove the part-00000 we got from the last iteration in order to replace it with the next one
            remove_part_00000 = subprocess.run(["rm", "-r", "files/LocalHadoopOutput/part-00000"])
        # If the centers have converged, end the algo and print the final coordinates of the centers
        else:
            # delete the part_00000 from local directory
            remove_part_00000 = subprocess.run(["rm", "-r", "files/LocalHadoopOutput/part-00000"])
            # Print a small report with the results of the operation
            print()
            print("The Map - Combine - Reduce process ended succesfully!")
            print("The final calculated coordinates of the centers are: ")
            for i in range(len(new_centers)):
                print("Cluster " + str(i) + ": " + str(new_centers[i]))
