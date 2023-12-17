# This code is intended to parse the file and create the c_Person objects.
from c_Person import c_Person
import numpy as np

# This function parses the file and creates the c_Person objects.
def parse(file):
    n = 0
    m = 0
    personnes = []
    with open(file, 'r') as f:
        # Read the first line and split the values.
        n, m = map(int, f.readline().split())
        # n lines are the people.
        for _ in range(n):
            id, weight = map(int, f.readline().split())
            # Create the c_Person object and add it to the list.
            personnes.append(c_Person(id, weight, n))
        # m lines are the relations.
        for _ in range(m):
 
            id1, id2 = map(int, f.readline().split())
            # Add the relation to both people.
            personnes[id1].add_relation(personnes[id2])
            personnes[id2].add_relation(personnes[id1])
        for personne in personnes:
            # Calculate the weight heuristic for each person.
            personne.calculate_weight_heur()
    return np.array(personnes)