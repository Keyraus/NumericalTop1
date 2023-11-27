import numpy as np
from personne import Personne
from personne_parser import parse

def glouton(personnes):
    C = np.array(personnes)
    S = np.array([])

    while len(C) > 0:
        i = heuristic(C, S)
        if i == -1:
            break
        S = np.append(S, C[i])
        C = np.delete(C, i)

    score = 0
    for i in S:
        score += i.weight
        line = "Personne %d (%d) (%d)" % (i.id, i.weight, len(i.relations))
        for relation in i.relations:
            line += " %d, " % relation.id
        line += "]"
        print(line)
    print("\nScore : %d" % score)
    return score

def heuristic(C, S):
    max = -1
    index = -1
    for C_i in C:
        canInvite = True
        for S_j in S:
            if not S_j.is_friend(C_i):
                canInvite = False
                break
        if not canInvite:
            continue

        value = C_i.weight * len(C_i.relations)
        if value > max:
            max = value
            index = np.where(C == C_i)[0][0]
   
    return index


