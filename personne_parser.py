# This code is intended to parse the file and create the Personne objects.
from personne import Personne
import numpy as np

def parse(file):
    n = 0
    m = 0
    personnes = []
    
    with open(file, 'r') as f:
        n, m = map(int, f.readline().split())
        for _ in range(n):
            id, weight = map(int, f.readline().split())
            personnes.append(Personne(id, weight))
        for _ in range(m):
            id1, id2 = map(int, f.readline().split())
            personnes[id1].add_relation(personnes[id2])
            personnes[id2].add_relation(personnes[id1])
    return np.array(personnes)