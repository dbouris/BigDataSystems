import csv
from neo4j import GraphDatabase

# Connect to Neo4j
Driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))

def load_mooc_actions_to_neo4j(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            user = row['USERID']
            action = row['ACTIONID']
            target = row['TARGETID']
            timestamp = row['TIMESTAMP']

            with Driver.session() as session:
                session.run("""
                    MERGE (u:User {userID: $user})
                    MERGE (a:Action {actionID: $action, timestamp: $timestamp})
                    MERGE (t:Target {targetID: $target})
                    MERGE (u)-[:PERFORMS]->(a)
                    MERGE (a)-[:ON]->(t)
                """, user=user, action=action, target=target, timestamp=timestamp)

def load_mooc_action_features_to_neo4j(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            action = row['ACTIONID']
            feature0 = float(row['FEATURE0'])
            feature1 = float(row['FEATURE1'])
            feature2 = float(row['FEATURE2'])
            feature3 = float(row['FEATURE3'])

            with Driver.session() as session:
                session.run("""
                    MATCH (a:Action {actionID: $action})
                    SET a.feature0 = $feature0, a.feature1 = $feature1, 
                        a.feature2 = $feature2, a.feature3 = $feature3
                """, action=action, feature0=feature0, feature1=feature1, 
                     feature2=feature2, feature3=feature3)


def load_mooc_action_labels_to_neo4j(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            action = row['ACTIONID']
            label = row['LABEL']

            with Driver.session() as session:
                session.run("""
                    MATCH (a:Action {actionID: $action})
                    SET a.label = $label
                """, action=action, label=label)


load_mooc_actions_to_neo4j('Data\mooc_actions.tsv')
print('mooc_actions.tsv loaded')
load_mooc_action_features_to_neo4j('Data\mooc_action_features.tsv')
print('mooc_action_features.tsv loaded')
load_mooc_action_labels_to_neo4j('Data\mooc_action_labels.tsv')
print('mooc_action_labels.tsv loaded')

