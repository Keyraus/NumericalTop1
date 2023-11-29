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
        #print(line)
    #print("\nScore : %d" % score)
    return score

def heuristic(C, S):
    max = -1
    index = -1
    for C_i in C:
        canInvite = True
        for S_j in S:
            #try to find the id of C_i in S_j.relations
            #if not found, canInvite = False


            if not S_j.is_friend(C_i):
                canInvite = False
                break
            ##print("canInvite : ", canInvite)
        if not canInvite:
            continue
        ##print all the invited people in S
        #for i in S:
            #print(i.id, end=" ")
        #print("C_i : ", C_i.id)
        value = C_i.weight * len(C_i.relations)
        if value > max:
            max = value
            index = np.where(C == C_i)[0][0]
    return index
def gloutonRandomGen(personnes):
    C = np.array(personnes)

    S = np.array([])
    #choose random person
    i = np.random.randint(0, len(C))
    #print(C[i])
    C[i].invited = True
    S = np.append(S, C[i])
    C = np.delete(C, i)
    #print("pouet", S[0].id)
    while len(C) > 0:
        i = heuristic(C, S)
        if i == -1:
            break
        C[i].invited = True
        S = np.append(S, C[i])
        C = np.delete(C, i)

    #return S + C in the ascending order of id
    S = np.append(S, C)
    S = sorted(S, key=lambda personne: personne.id)
    ##print le score de S
    score = 0
    for i in S:
        if i.invited:
            score += i.weight
    #print("\nScore : %d" % score)
    
    ##print all the invited people in S

    for i in S:
        if i.invited:
            line = "Personne %d (%d) (%d)" % (i.id, i.weight, len(i.relations))
            #print(line)
            ##print(i)
    return S

def gloutonGen(personnes):
    C = np.array(personnes)
    S = np.array([])

    while len(C) > 0:
        i = heuristic(C, S)
        if i == -1:
            break
        C[i].invited = True
        S = np.append(S, C[i])
        C = np.delete(C, i)

    #return S + C in the ascending order of id
    S = np.append(S, C)
    S = sorted(S, key=lambda personne: personne.id)
    ##print le score de S
    score = 0
    for i in S:
        if i.invited:
            score += i.weight
    
    return S
