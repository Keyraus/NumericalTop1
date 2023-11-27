import glouton
import os
import sys
from personne_parser import parse
import numpy as np
import algo_genetique as ag

def main():
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if "Objective:  z =" in line:
                result = line.split("Objective:  z = ")[1].split(" ")[0]
                break
    # Print the result
    print("Resulat attendu", result)
    score = glouton.glouton(parse(sys.argv[1]))

    gap = (int(result) - score) / int(result)
    print("Gap : %f" % gap)

    ####################################################################################
    # Utilisation de l'algo de bron-kerbosch
    # all_clique = glouton.find_all_cliques(possible_node_to_append=parse(sys.argv[1]))
    # print("Nombre de clique : %d" % len(all_clique))
    # best_clique = max(all_clique, key=lambda x: sum([i.weight for i in x]))
    # print(person.id for person in best_clique)
    # print("Poids de la clique : %d" % sum([i.weight for i in best_clique]))

    #score2 = ag.intialisation_population(parse(sys.argv[1]), 1000)
    #print("Score2 : %d" % np.mean(score2))

if __name__ == "__main__":
    main()
