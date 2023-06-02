## Project Overview
In this project, we focus on analyzing and understanding user behavior data from Massive Open Online Courses (MOOCs) platforms. The key unit of our analysis is an "action" which represents an interaction of a user with the MOOC platform. Actions are performed by users on targets. In the MOOC context, a "target" can be a course, a lecture, a quiz, or any other entity in the MOOC.

The interactions form a complex network, where users, actions, and targets are interconnected. To efficiently handle and analyze this complex network data, we have chosen to use a graph database, Neo4j. The primary reason for this choice is the powerful querying capabilities of Neo4j and its ability to handle complex, highly connected data.

In our Neo4j database, we have nodes representing Users, Actions, and Targets. Actions are connected to Users and Targets through relationships, indicating which user performed the action and on which target.

This project involves the following main steps:

1. Data Loading: We load the data from three separate TSV files into the Neo4j database using Python's official Neo4j driver. These files contain information about users, their actions, and the targets of these actions.

1. Querying: We have designed and implemented a series of Cypher queries to analyze the graph. These queries help to uncover patterns such as the count of all users, targets, actions, the actions and targets of specific users, the number of actions per user, etc.

1. Benchmarking: We time the execution of each query to understand the query's performance. This gives us insights into how efficiently we can retrieve information from our graph database.

The insights derived from these queries can help in understanding user behavior patterns and can inform design decisions for MOOC platforms to enhance user engagement and satisfaction. It also serves as a performance benchmarking exercise to understand the scalability of Neo4j queries for larger datasets.

## How to Run the Code

1. Install the required Python package: Neo4j

You can install these package using pip:
```
pip install neo4j 
```
2. Install and set up Neo4j:

* Download the latest version of Neo4j from the official [Neo4j download page](https://neo4j.com/download/). You may choose either the Community Edition or Enterprise Edition for this project.

Once downloaded, follow the installation instructions for your specific operating system.

* After the installation, open the Neo4j Desktop application and create a new database. Set a password for the database - you'll need this to connect your Python script to the database.

* Start the database.

* Note down the bolt URL and the password for the database, you'll need this for the Python script to connect to the database.

3. Run the <b>data_loading.py</b> script to load the data into the Neo4j database:

* Update the bolt URL, username, and password in the Python script to match your Neo4j database's credentials.

* Make sure your TSV files are in the same directory as your Python script, or update the file paths in the script to match your file locations.

* Run the script.

4. Run the <b>benchmarking.py</b> script to execute the queries and time their performance:

* Similar to the data_loading.py script, make sure the bolt URL, username, and password in the benchmarking.py script match your Neo4j database's credentials.

* Run the script.

By following these steps, you should be able to successfully run the code and see the results of the analysis and benchmarking.

## Dataset
The data used in this project originates from a Massive Open Online Course (MOOC) platform. It comprises user actions logged in three separate tab-separated values (TSV) files:

1. 'mooc_actions.tsv' - This file contains the main action logs. Each row represents an action performed by a user on a certain target (such as a course or a page). The file contains the following columns:

* User ID
* Action ID
* Target ID
* Timestamp

2. 'mooc_action_features.tsv' - This file includes additional features for each action. It contains the following columns:

* Action ID
* Feature 1
* Feature 2
* Feature 3
* Feature 4

3. 'mooc_action_labels.tsv' - This file includes labels for each action. The columns are:

* Action ID
* Label

The main purpose of this project is to import this data into a Neo4j graph database and perform various queries and analyses on it. The graph structure allows us to easily represent and analyze the relationships between users, actions, and targets.

## Queries and Benchmark Analysis

Once the data is loaded into the Neo4j graph database, we perform a series of Cypher queries to extract and analyze information from the graph. Here's an overview of each query along with an analysis of its benchmark timing:

1. Display a small portion of the graph database: This query retrieves 10 User nodes, their PERFORMS relationships, the associated Action nodes, the ON relationships, and the connected Target nodes. This gives a quick snapshot of the graph structure and content. The execution time is typically short as it only retrieves a small subset of the entire graph. (Execution Time: 2.07775 seconds)

1. Count all users, targets, and actions: This query is used to get a high-level overview of the data volume in the graph. It separately matches all User, Target, and Action nodes and counts them. The execution time depends on the size of the graph. (Execution Time: 0.01599 seconds)

1. Show all actions and targets of a specific user: This query retrieves all actions performed by a specific user and the associated targets. The execution time will typically depend on the number of actions performed by the user. (Execution Time: 0.00179 seconds)

1. For each user, count their actions: This query groups actions by user and counts the number of actions per user. Execution time generally depends on the total number of users and actions in the graph. (Execution Time: 0.00094 seconds)

1. For each target, count how many users have performed actions on it: This query calculates the number of distinct users that have performed actions on each target. Execution time will typically depend on the total number of targets and actions in the graph. (Execution Time: 0.00001 seconds)

1. Count the average actions per user: This query calculates the average number of actions performed by each user. This can help in understanding the overall user engagement with the platform. (Execution Time: 0.00100 seconds)

1. Show the userID and the targetID, if the action has positive Feature2: This query finds all the user-target pairs where the associated action has a positive feature2 value. The execution time for this query will typically depend on the total number of actions with positive feature2 in the graph. (Execution Time: 0.00117 seconds)

1. For each targetID, count the actions with label “1”: This query counts the number of actions with a label "1" for each target. The execution time of this query will generally depend on the number of actions with label "1" in the graph. (Execution Time: 0.00001 seconds)

As the benchmark results suggest, execution times for the queries vary based on the complexity of the query and the volume of data involved. Queries involving counts or operations on a large number of nodes or relationships generally take more time than queries working on a smaller subset of data or performing simpler operations. This provides valuable insights into the performance of Neo4j graph databases and can guide further optimization of the data model and query design.
