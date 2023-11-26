# This code is intended to parse the file and create the Personne objects.
from personne import Personne
import numpy as np

def parse(file):
    n = 0
    m = 0
    personnes = np.array([])
    relations = np.array([])

    with open(file, 'r') as f:
        n, m = map(int, f.readline().split())
        for i in range(n):
            id, weight = map(int, f.readline().split())
            personnes = np.append(personnes, Personne(id, weight))
        for i in range(m):
            id1, id2 = map(int, f.readline().split())
            relations = np.append(relations, [(id1, id2)]).reshape(-1, 2)
            personnes[id1].add_relation(personnes[id2])
            personnes[id2].add_relation(personnes[id1])
    return personnes