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
    
    C[i].invited = True
    S = np.append(S, C[i])
    C = np.delete(C, i)
    
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

def gloutonV2(dict,gen = False, IsRandom = False):

    list_personnes = [i for i in range(len(dict))]
    S = [0 for _ in list_personnes]

    #init S with the person with the higher weight_heur
    max_weight = 0
    index = 0
    if IsRandom:
        index = np.random.randint(0, len(list_personnes))
    else:
        for personne in list_personnes:
            if dict[personne].weight_heur > max_weight:
                max_weight = dict[personne].weight_heur
                index = personne

    S[index] = 1
    list_personnes.remove(index)

    while len(list_personnes) > 0:
        i = heuristicV2(dict, S, IsRandom)
        if i == -1:
            break
        
        S[i] = 1
        #print("S: ", np.nonzero(S)[0])
        #print(list_personnes)
        list_personnes.remove(i)

    score = 0
    line = ""
    for personne in dict:
        if S[personne.id] == 1:
            score += personne.weight
            line = "Personne %d (%d) (%d)" % (personne.id, personne.weight, len(personne.relations))
        for relation in dict[i].relations:
            line += " %d, " % relation.id
        line += "]"
        #print(line)
    if gen:
        return S
    else :
        return score


def heuristicV2(dict, S, random = False):
    if not random:
        print("S: ", np.nonzero(S)[0])
        max = -1
        index = -1
        first_index = np.nonzero(S)[0][0]
        for personne in dict[first_index].relations:
            if S[personne.id] == 1:
                continue

            value = personne.weight * len(dict[personne.id].relations)
            #print(personne.id, "value: ", value )
            if personne.id == 295 or personne.id == 161:
                print(personne.id, value)
            if value > max:
                for invited in np.nonzero(S)[0]:
                    if not dict[invited].is_friend(personne):
                        break
                else:
                    max = value
                    index = personne.id
        return index
    else:
        max = -1
        index = -1
        first_index = np.nonzero(S)[0][0]
        proba_array = np.array([])
        people_array = np.array([])
        total = 0
        sumTotal = 0
        # calculate sum of all the weight_heur of the friends of the first person
        for personne in dict[first_index].relations:
            if S[personne.id] == 1:
                # person is already invited
                continue
            # check if everyone in S is friend with personne
            for invited in np.nonzero(S)[0]:
                if not dict[invited].is_friend(personne):
                    break
            else:
                # everyone in S is friend with personne
                sumTotal += personne.weight * len(dict[personne.id].relations)
                people_array = np.append(people_array, int(personne.id))

        # I want that for each relation of first index, if the person is already invited, then I put -1 in proba_array, else I put the proba
        # I need to have a proba_array with same size as dict[first_index].relations to get the true index of the person
        #print(len(dict[first_index].relations))
        
        for people in dict[first_index].relations:
            people = dict[int(people.id)]
            if people.id in people_array:
                proba = people.weight_heur / sumTotal
                proba_array = np.append(proba_array, total + proba)
                total += proba
            else:
                proba_array = np.append(proba_array, -1)
        #print(len(proba_array))

        # calculate proba in interval [0,1] to invite a person
        # check if proba array is empty
        # if yes, then we can't invite anyone else so we return -1
        # I need to have a proba_array with same size as dict[first_index].relations to get the true index of the person
        if len(proba_array) == 0 or len(people_array) == 0:
            return -1
        rand = np.random.random()
        #print("rand: ", rand)
        #print("total: ", people_array)
        #print("proba_array: ", proba_array)
        personne = 0
        for proba_1 in proba_array:
            if proba_1 > rand:
                break
            personne += 1
        personne = dict[first_index].relations[personne].id
        index = personne
        #print("personne: ", personne)
        #print(np.nonzero(S)[0])
        return index


def gloutonVTest(dict,gen = False, IsRandom = False):
    list_personnes = [i for i in range(len(dict))]
    S = [0 for _ in list_personnes]
    print("Sdebutgloutn: ", np.nonzero(S)[0])
    #init S with the person with the higher weight_heur
    max_weight = 0
    index = 0


    while len(list_personnes) > 0:
        i = heuristicV2(dict, S, IsRandom)
        if i == -1:
            break
        
        S[i] = 1
        list_personnes.remove(i)

    score = 0
    line = ""
    for personne in dict:
        if S[personne.id] == 1:
            score += personne.weight
            line = "Personne %d (%d) (%d)" % (personne.id, personne.weight, len(personne.relations))
        for relation in dict[i].relations:
            line += " %d, " % relation.id
        line += "]"
        #print(line)
    if gen:
        return S
    else :
        return score