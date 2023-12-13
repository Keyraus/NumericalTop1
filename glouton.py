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
