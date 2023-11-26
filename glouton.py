import numpy as np
from personne import Personne
from personne_parser import parse

def glouton(personnes):
    C = np.array(personnes)
    S = np.array([])
    for i in C:
        if i.id == 178 or i.id == 101 or i.id == 218 or i.id == 223 or i.id == 269:
            print(i.id, i.weight, len(i.relations))

    while len(C) > 0:
        i = heuristic(C, S)
        if i == -1:
            break
        S = np.append(S, C[i])
        C = np.delete(C, i)
        for j in C:
            j.remove_relation(C[i])

    score = 0
    for i in S:
        score += i.weight
        line = "Personne %d (%d) (%d)" % (i.id, i.weight, len(i.relations))
        for relation in i.relations:
            line += "%d, " % relation.id
        line += "]"
        print(line)
    print("Score : %d" % score)
    return score

def heuristic(C, S):
    max = -1
    index = -1
    print(S)
    for C_i in C:
        canInvite = True
        for S_j in S:
            if not C_i.is_friend(S_j):
                canInvite = False
                break
        if not canInvite:
            continue
        value = C_i.weight * len(C_i.relations)
        if value > max:
            max = value
            index = np.where(C == C_i)[0][0]
    return index


