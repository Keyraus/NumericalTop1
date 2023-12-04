import glouton
import os
import sys
import time
from personne_parser import parse
import numpy as np
import algo_genetique as ag

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 main.py instance.txt solution.txt")
        sys.exit(1)
    # check if the instance file exists
    if not os.path.exists(sys.argv[1]):
        print("Error: file '%s' not found" % sys.argv[1])
        sys.exit(1)
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if "Objective:  z =" in line:
                result = line.split("Objective:  z = ")[1].split(" ")[0]
                break
    chosenOption = input("Choisissez l'option :\n1. Glouton\n2. Algo génétique\n3. Bron-Kerbosch\n4. Tous\n")
    print("Option choisie : %s" % chosenOption)
    print("Résultat de l'instance GLPK : %s" % result)
    actualTime = time.time()
    if chosenOption == "1":
        score = glouton.glouton(parse(sys.argv[1]))
        print("Score : %d" % score)
    elif chosenOption == "2":
        print("ToDo")
    elif chosenOption == "3":
        ####################################################################################
        # Utilisation de l'algo de bron-kerbosch
        # all_clique = glouton.find_all_cliques(possible_node_to_append=parse(sys.argv[1]))
        # print("Nombre de clique : %d" % len(all_clique))
        # best_clique = max(all_clique, key=lambda x: sum([i.weight for i in x]))
        # print(person.id for person in best_clique)
        # print("Poids de la clique : %d" % sum([i.weight for i in best_clique]))
        #score2 = ag.intialisation_population(parse(sys.argv[1]), 1000)
        #print("Score2 : %d" % np.mean(score2))
        
        # all_clique = glouton.find_all_cliques(possible_node_to_append_to_the_clique=parse(sys.argv[1]))
        # print("Nombre de clique : %d" % len(all_clique))
        # best_clique = max(all_clique, key=lambda x: sum([i.weight for i in x]))
        # print([person.id for person in best_clique])
        # score = sum([i.weight for i in best_clique])
        # print("Poids de la clique : %d" % score)

        max_clique = glouton.find_maximum_clique(possible_node_to_append_to_the_clique=parse(sys.argv[1]))
        print([person.id for person in max_clique])
        score = sum([i.weight for i in max_clique])
        print("Poids de la clique : %d" % score)

    elif chosenOption == "4":
        score = glouton.glouton(parse(sys.argv[1]))
        print("Score : %d" % score)
        score2 = ag.intialisation_population(parse(sys.argv[1]), 1000)
        print("Score2 : %d" % np.mean(score2))
        all_clique = glouton.find_all_cliques(possible_node_to_append=parse(sys.argv[1]))
        print("Nombre de clique : %d" % len(all_clique))
        best_clique = max(all_clique, key=lambda x: sum([i.weight for i in x]))
        print(person.id for person in best_clique)
        print("Poids de la clique : %d" % sum([i.weight for i in best_clique]))
    else:
        print("Option invalide")
    # print the gap
    print("Gap : %f" % ((int(result) - score) / int(result)))
    print("Temps d'exécution : %f" % (time.time() - actualTime))

    

if __name__ == "__main__":
    main()
