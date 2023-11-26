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
        line = "Personne %d (%d) (%d) : [" % (i.id, i.weight, len(i.relations))
        for relation in i.relations:
            line += "%d, " % relation.id
        line += "]"
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
    for i in range(len(C)):
        personne = C[i]
        # Check if the personne is already invited
        if personne.invited:
            continue
        # Check if the personne knows everyone in S
        # If yes, we can invite him
        # If no, we can't invite him
        canInvite = True
        for j in range(len(S)):
            personne2 = S[j]
            if not personne.is_friend(personne2):
                canInvite = False
                break
        if not canInvite:
            continue
        # Compute the value of the personne
        value = C[i].weight * len(C[i].relations)
        # Check if the value is higher than the max
        if value > max:
            max = value
            index = i
    return index
    
def update(C, i):
    # Update the C tab
    return np.delete(C, i)


