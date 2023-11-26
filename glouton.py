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
        C = update(C, i)
    # Print the solution
    # Print the solution tab with the weight of each personne invited
    # Condition on if the personne is invited or not
    score = 0
    for i in S:
        score += i.weight
        line = "Personne %d (%d) (%d)" % (i.id, i.weight, len(i.relations))
        #for relation in i.relations:
        #    line += "%d, " % relation.id
        #line += "]"
        print(line)
    # Print the score
    print("Score : %d" % score)
    return score

def heuristic(C, S):
    # Compute the heuristic
    # Return the index of the personne with the best heuristic
    # Return -1 if there is no personne to invite
    max = -1
    index = -1
    print(S)
    for C_i in C:
        # Check if the personne knows everyone in S
        # If yes, we can invite him
        # If no, we can't invite him
        canInvite = True
        for S_j in S:
            #if Ci is 8 or 120 print the id of the personne in S
           # if C_i.id == 8 or C_i.id == 120 or C_i.id == 85 or C_i.id == 161:
               # print(C_i.id, S_j.id)
               # print(C_i.is_friend(S_j))
            if not C_i.is_friend(S_j):
                canInvite = False
                break
        if not canInvite:
            continue
        # Compute the value of the personne in C with the personnes in S
        #the value of C_i is the sum of the weight of the relations of C_i that know everyone the first element in S
        value = C_i.weight
        value2 = 0
        for relation in C_i.relations:
            #check if the relation know the first element in S
            for S_j in S:
                if relation.is_friend(S_j):
                    #set the value to the higher wieght of the relation
                    if relation.weight > value2:
                        value2 = relation.weight
                        #mulitplie the value 2 by the number of relations that relation has with S_j
                        value2 *= len(relation.relations)
                        value3 = 0
                        for relation2 in relation.relations:
                            #check if the relation know the first element in S
                            for S_j in S:
                                if relation2.is_friend(S_j):
                                    #set the value to the higher wieght of the relation
                                    if relation2.weight > value3:
                                        value3 = relation.weight
                        value2 *= value3
        
        value += value2  / 100000
        
        # Check if the value is higher than the max
        if value > max:
            max = value
            #return the incex of the personne in C
            index = np.where(C == C_i)[0][0]
    return index
    
def update(C, i):
    # Update the C tab
    return np.delete(C, i)


