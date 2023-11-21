# This code is intended to parse the file and create the Personne objects.
from personne import Personne


def parse(file):
    # The first line contains n and m, respectively the number of people and the number of relations.
    # The following n lines contain the id and the weight of each person.
    # The following m lines contain the id of the two people involved in the relation.
    # If a relation is given in the file, it means that the two people are friends.
    n = 0
    m = 0
    personnes = []
    relations = []

    with open(file, 'r') as f:
        n, m = map(int, f.readline().split())
        for i in range(n):
            id, weight = map(int, f.readline().split())
            personnes.append(Personne(id, weight))
        for i in range(m):
            id1, id2 = map(int, f.readline().split())
            relations.append((id1, id2))
    for id1, id2 in relations:
        personnes[id1].add_relation(personnes[id2])
        personnes[id2].add_relation(personnes[id1])
    return personnes