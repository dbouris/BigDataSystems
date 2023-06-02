import time
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))

def benchmark_query(query, query_number):
    with driver.session() as session:
        start_time = time.time()

        result = session.run(query)

        end_time = time.time()

        output = f"\nQuery {query_number} executed in {end_time - start_time} seconds."

        return result.values(), output


# Define the queries
queries = [
    # 1. Show a small portion of your graph database (screenshot)
    ''' 
    MATCH (u:User)-[p:PERFORMS]->(a:Action)-[o:ON]->(t:Target)  
    RETURN u, p, a, o, t LIMIT 10 
    ''',
    # 2. Count all users, count all targets, count all actions
    '''
    MATCH (u:User)
    WITH count(u) as UserCount
    MATCH (t:Target)
    WITH UserCount, count(t) as TargetCount
    MATCH (a:Action)
    RETURN UserCount, TargetCount, count(a) as ActionCount
    ''',
    # 3. Show all actions (actionID) and targets of a specific user (6978)
    '''
    MATCH (u:User {userID: "6978"})-[:PERFORMS]->(a:Action)-[:ON]->(t:Target)
    RETURN a.actionID as ActionID, t.targetID as TargetID
    ''',
    # 4.  For each user, count his/her actions
    '''
    MATCH (u:User)-[:PERFORMS]->(a:Action)
    RETURN u.userID as UserID, count(a) as ActionCount
    ''',
    # 5. For each target, count how many users have done this target
    '''
    MATCH (u:User)-[:PERFORMS]->(a:Action)-[:ON]->(t:Target)
    RETURN t.targetID as TargetID, count(DISTINCT u) as UserCount
    ''',
    # 6. Count the average actions per user
    '''
    MATCH (u:User)-[:PERFORMS]->(a:Action)
    WITH u, count(a) as ActionCount
    RETURN avg(ActionCount) as AvgActions
    ''',
    # 7. Show the userID and the targetID, if the action has positive Feature2
    '''
    MATCH (u:User)-[:PERFORMS]->(a:Action)-[:ON]->(t:Target)
    WHERE a.feature2 > 0
    RETURN u.userID as UserID, t.targetID as TargetID
    ''',
    # 8. For each targetID, count the actions with label “1”*
    '''
    MATCH (a:Action {label: "1"})-[o:ON]->(t:Target)
    RETURN t.targetID as TargetID, count(a) as ActionCount
    '''
]

# Open output file
with open('benchmark_output.txt', 'w') as f:
    # Benchmark the queries
    for i, query in enumerate(queries):
        result, output = benchmark_query(query, i+1)
        f.write(output + '\n')
        for record in result:
            f.write(str(record) + '\n')

driver.close()
