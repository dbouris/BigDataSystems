#!/usr/bin/env python

"""
generateDataset.py: contains a method which generates synthetic data
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs

def generateDataPoints(dataset_size, centers, export_path):

    """
    The function generates a dataset of 2D data points using scikit-learn's make_blobs method.
    The function takes three input parameters: dataset_size, centers, and export_path
    """

    # Generate the data points by following normal distribution
    X, labels = make_blobs(n_samples=dataset_size, centers=centers,
    cluster_std=6.0, n_features=2)
    # round the values and save them in a pandas dataframe
    X = np.round(X, 1)
    points = pd.DataFrame(X)
    # export the dataset 
    points.to_csv(export_path, sep=',', index=False, header=False)


if __name__ == "__main__":
    
    # specify the number of rows to generate
    rows = 1200000
    # specify the centers around which we want the data to be formed
    centers = [[-100000, -100000], [1, 1], [100000, 100000]]
    # specify the export path
    export_path = "data-points.csv"

    generateDataPoints(rows, centers, export_path)