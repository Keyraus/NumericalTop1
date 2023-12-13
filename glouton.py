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
            line += " %d, " % relation
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
    
    C[i].invited = 1
    S = np.append(S, C[i])
    C = np.delete(C, i)
    
    while len(C) > 0:
        i = heuristic(C, S)
        if i == -1:
            break
        C[i].invited = 1
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
        C[i].invited = 1
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

    list_personnes = [i for i, _ in enumerate(dict)]
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
        i = heuristicV2(dict, S, False)
        if i == -1:
            break
        S[i] = 1
        list_personnes.remove(i)

    score = 0

    for i in np.nonzero(S)[0]:
        score += dict[i].weight
    if gen:
        return S
    else :
        return score


def heuristicV2(dict, S, random = False):
    if not random:
        max = -1
        index = -1
        first_index = np.nonzero(S)[0][0]
        indexinsolution = np.nonzero(S)[0]
        
        for personne in np.nonzero(dict[first_index].relations)[0]:
            value = dict[personne].weight_heur * (not S[personne])

            if value > max:
                for invited in indexinsolution:
                    if not dict[invited].relations[personne]:
                        break
                else:
                    max = value
                    index = personne
        return index
    else:
        max = -1
        index = -1
        first_index = np.nonzero(S)[0][0]
        proba_array = np.array([])
        people_array = np.array([])
        total = 0
        sumTotal = 0

        for personne in dict[first_index].relations:
            if S[personne] == 1:
                continue

            for invited in np.nonzero(S)[0]:
                if not dict[invited].is_friend(personne):
                    break
            else:

                sumTotal += dict[personne].weight * len(dict[personne].relations)
                people_array = np.append(people_array, int(personne))

        for people in dict[first_index].relations:
            people = dict[int(people)]
            if people.id in people_array:
                proba = people.weight_heur / sumTotal
                proba_array = np.append(proba_array, total + proba)
                total += proba
            else:
                proba_array = np.append(proba_array, -1)

        if len(proba_array) == 0 or len(people_array) == 0:
            return -1
        rand = np.random.random()
        personne = 0
        for proba_1 in proba_array:
            if proba_1 > rand:
                break
            personne += 1

        return dict[first_index].relations[personne].id


def gloutonVTest(dict,gen = False, IsRandom = False):
    list_personnes = [i for i in range(len(dict))]
    S = [0 for _ in list_personnes]
    print("Sdebutgloutn: ", np.nonzero(S)[0])
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
# Bron-Kerbosch algorithm
def find_all_cliques(current_clique=[], possible_node_to_append_to_the_clique=[], impossible_node_to_append_to_the_clique=[]):
    if len(possible_node_to_append_to_the_clique) == 0 and len(impossible_node_to_append_to_the_clique) == 0:
        return [current_clique]

    all_cliques = []
    for node in possible_node_to_append_to_the_clique:
        # Find all the nodes that are friends with the current node
        new_possible_node_to_append = [n for n in possible_node_to_append_to_the_clique if n.is_friend(node)]
        # The node is then impossible to append to the clique because it is already in it
        new_impossible_node_to_append = [n for n in impossible_node_to_append_to_the_clique if n.is_friend(node)]

        # Add the node to the clique
        new_current_clique = current_clique + [node]
        # Call the algorithm recursively
        all_cliques += find_all_cliques(new_current_clique, new_possible_node_to_append, new_impossible_node_to_append)

        # Remove the node from the list
        possible_node_to_append_to_the_clique = [n for n in possible_node_to_append_to_the_clique if n != node]
        impossible_node_to_append_to_the_clique.append(node)

    return all_cliques


# Same method but returns the maximum clique based on the weight of the nodes
def find_maximum_clique(current_clique=[], possible_node_to_append_to_the_clique=[], impossible_node_to_append_to_the_clique=[]):
    if len(possible_node_to_append_to_the_clique) == 0 and len(impossible_node_to_append_to_the_clique) == 0:
        return current_clique

    max_clique = []
    for node in possible_node_to_append_to_the_clique:
        # Find all the nodes that are friends with the current node
        new_possible_node_to_append = [n for n in possible_node_to_append_to_the_clique if n.is_friend(node)]
        # The node is then impossible to append to the clique because it is already in it
        new_impossible_node_to_append = [n for n in impossible_node_to_append_to_the_clique if n.is_friend(node)]

        # Add the node to the clique
        new_current_clique = current_clique + [node]
        # Call the algorithm recursively
        new_max_clique = find_maximum_clique(new_current_clique, new_possible_node_to_append, new_impossible_node_to_append)

        if sum(personne.weight for personne in new_max_clique) > sum(personne.weight for personne in max_clique):
            max_clique = new_max_clique

        # Remove the node from the list
        possible_node_to_append_to_the_clique = [n for n in possible_node_to_append_to_the_clique if n != node]
        impossible_node_to_append_to_the_clique.append(node)

    return max_clique
