# Assignment Description

In this assignment, the core objective is to implement the KMeans Clustering Algorithm in a Haddoop environment. More specificaly, the Mapper and Reducer functions should be implemented. A detailed description of the assignment can be found [here](files/Proj2_Hadoop.pdf).

# Hadoop Insallation

The installation of Hadoop on our local machine (Mac M1) was done according to the following instructions:
- [Article 1](https://codewitharjun.medium.com/install-hadoop-on-macos-m1-m2-6f6a01820cc9)
- [Article 2](https://blog.contactsunny.com/data-science/installing-hadoop-on-the-new-m1-pro-and-m1-max-macbook-pro)
- [YouTube Video](https://www.youtube.com/watch?v=inDC9jgwpWY&t=1s)

Note: To succesfully install and configure hadoop localy, `python` and `java jdk` need to be installed.
Versions Used:
- `python 3.9.15`
- `java jdk1.8.0_361`

# Implementation 

For implementing the KMeans Clustering algorithm in a Hadoop, the programming paradigm Map - Combine - Reduce was used. Map - Combine - Reduce is a variation of the MapReduce programming model that adds an additional "combine" phase between the "map" and "reduce" phases. The "combine" phase is similar to the "reduce" phase in that it aggregates key-value pairs.

More specificaly, the use and purpose of each phase in the KMeans implementation is described below:
- [Mapper](mapper.py) <br>
The mapping phase of the operation is responsible for assigning each input point to the optimal cluster, which is the cluster whose center is the nearest (Manhattan distance). 
    - Output Shape: `num_cluster    [x,y]`

- [Combiner](combiner.py) <br>
The combiner is responsible for calculating foreach cluster the sum of the x and y coordinates of the points which have been assigned to it. The combiner takes as input the output of the mapper pahse.
    - Input Shape: `num_cluster    [x,y]`
    - Output Shape: `num_cluster ([subsum_x, subsum_y], num_points_participated)`

- [Reducer](reducer.py) <br>
The reducer is responsible for calculating the new centers of each cluster. The new cluster center is calculated as the average of x and y coordinates of the items that have been assigned to each cluster. The reducer uses as input the output of the combination phase.
    - Input Shape: `num_cluster ([subsum_x, subsum_y], num_points_participated)`
    - Output Shape: `[new_center_x, new_center_y]`

- [KMeans](KMeans.py) <br>
The `KMeans.py` is the 'coordinator' and is responsible for connecting to the local Hadoop nodes and starting the MapReduce job. 





