import numpy as np
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
        new_possible_node_to_append = [n for n in possible_node_to_append_to_the_clique if node in np.nonzero(n.relations)[0]]
        # The node is then impossible to append to the clique because it is already in it
        new_impossible_node_to_append = [n for n in impossible_node_to_append_to_the_clique if node in np.nonzero(n.relations)[0]]

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