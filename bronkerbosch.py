# Imports
import numpy as np

# This method perform bron-kerbosch algorithm to find all cliques
# Input: current_clique, the list of persons that are currenlty in the clique
#        possible_node_to_append_to_the_clique, the list of persons that can be append to the current clique
#        impossible_node_to_append_to_the_clique, the list of persons that can't be append to the current clique
# Ouput: all_cliques, a list of all cliques found by the algorithm
def find_all_cliques(current_clique=[], possible_node_to_append_to_the_clique=[], impossible_node_to_append_to_the_clique=[]):
    # If there are no more person that can be append to the clique
    if len(possible_node_to_append_to_the_clique) == 0 and len(impossible_node_to_append_to_the_clique) == 0:
        return [current_clique]

    all_cliques = []
    for node in possible_node_to_append_to_the_clique:
        # Find all the nodes that are friends with the current node
        new_possible_node_to_append = [n for n in possible_node_to_append_to_the_clique if n.relations[node.id] is True]
        # The node is then impossible to append to the clique because it is already in it
        new_impossible_node_to_append = [n for n in impossible_node_to_append_to_the_clique if n.relations[node.id] is True]

        # Add the node to the clique
        new_current_clique = current_clique + [node]
        # Call the algorithm recursively
        all_cliques += find_all_cliques(new_current_clique, new_possible_node_to_append, new_impossible_node_to_append)

        # Remove the node from the list
        possible_node_to_append_to_the_clique = [n for n in possible_node_to_append_to_the_clique if n != node]
        impossible_node_to_append_to_the_clique.append(node)

    return all_cliques