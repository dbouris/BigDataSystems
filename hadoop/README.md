# Assignment Description

In this assignment, the core objective is to implement the KMeans Clustering Algorithm in a Haddoop environment. More specificaly, the Mapper and Reducer functions should be implemented. A detailed description of the assignment can be found [here](files/Proj2_Hadoop.pdf).

# Hadoop Installation

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


# Running and testing KMeans on Hadoop

1. Generate the test dataset by running the `generateDataset.py` script which is located in the `/files` folder. A `data-points.csv` is the created.
    - The Python file contains the `generateDataPoints()` function which generates a dataset of 2D data points distributed around some pre-specified centers.

2. Start the hadoop clusters and move the data points file to the hdfs by running the commands below from the `/hadoop` directory of the project.

``` shell
$ start-all.sh # start all the daemons (processes) required to run a Hadoop cluster
$ hdfs dfs -mkdir /kmeans # create a directory to save the data points file
$ hdfs dfs -put files/data-points.csv /kmeans # move the data points file to hdfs
```

3. Then run the `KMeans.py`. The Map - Combine - Reduce is executed and the final cluster centers is printed. 

*Execution Notes:*
- To succesfully run the project the hadoop paths in the `KMeans.py` file need to be changed to match each installation
- Having in mind that the current implementation was configured and tested in a macOS operating system, running it in a different enviroment might need further adaptations.


# Execution Report and results
The KMeans Map - Combine - Reduce operation calculates the new centers after 3 iterations. The returned centers match with the pre-defined ones when the dataset was created, indicating that the KMeans ran succesfully and that the results are accurate. 

Below, the `all-centers.csv` file is presented. This file contains the different states of the centers foreach iteration. Each line represents the x and y coordinates of each center. Since we have 3 clusters (thus 3 centers) the first 3 lines represent the centers of the first iteration and so on. <br>
The 3 last coordinates which represent the centers in the last iteration of the KMeans algorithm match the pre-defined centers ([[-100000, -100000], [1, 1], [100000, 100000]]).

``` shell
# all-centers.csv

 -6.4, 5.9
 99996.0, 99998.7
 -3.0, -2.2
 0.0, 2.6
 61451.3, 61451.3
 -61450.7, -61452.3
 1.0, 1.0
 100000.0, 100000.0
 -100000.0, -100000.0
 1.0, 1.0
 100000.0, 100000.0
 -100000.0, -100000.0
```

Here is a snippet of the logs generated from the first KMeans and Map - Combine - Reduce operation. <br>
The full logs can be found [here](files/hadoop_output_logs.txt)


``` shell
...

2023-04-21 16:42:29,197 INFO mapred.Task: Final Counters for attempt_local868978880_0001_r_000000_0: Counters: 30
        File System Counters
                FILE: Number of bytes read=10885
                FILE: Number of bytes written=577409
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=18034485
                HDFS: Number of bytes written=54
                HDFS: Number of read operations=10
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=3
                HDFS: Number of bytes read erasure-coded=0
        Map-Reduce Framework
                Combine input records=0
                Combine output records=0
                Reduce input groups=3
                Reduce shuffle bytes=168
                Reduce input records=3
                Reduce output records=3
                Spilled Records=3
                Shuffled Maps =1
                Failed Shuffles=0
                Merged Map outputs=1
                GC time elapsed (ms)=0
                Total committed heap usage (bytes)=304611328
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Output Format Counters 
                Bytes Written=54
    ...
```

# References
- [Medium: MapReduce with Python](https://medium.com/geekculture/mapreduce-with-python-5d12a772d5b3)
- [MapReduce Jobs in Python](https://maelfabien.github.io/bigdata/MRJobP/#)
- [Mapreduce Python example](https://linuxhint.com/mapreduce-framework-python/)
- [GeeksForGeeks: MapReduce - Combiners](https://www.geeksforgeeks.org/mapreduce-combiners/)

# Acknowledgements
This project was created as part of Big Data Management Systems course at Department of Management Science & Technology in Athens University of Economics and Business
