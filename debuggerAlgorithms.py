# This program is intended to debug all the algorithms created for the project, several options are available for the user to choose from
# It takes in argument the instance file and the result file of the GLPK solver (not necessary but useful to compare the results)
import greedy
import sys
import time
from personne_parser import parse
import genetics as ag
import ant_colony_optimization as aco
import os
import time
import bronkerbosch as bk
def main():
    start = time.time()
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python3 debuggerAlgorithms.py instance.txt temps_en_secondes instance.lp")
        sys.exit(1)
    # check if the instance file exists
    if not os.path.exists(sys.argv[1]):
        print("Error: file '%s' not found" % sys.argv[1])
        sys.exit(1)
    # check if argument 2 is a number
    try:
        timeMax = int(sys.argv[2])
    except ValueError:
        print("Error: time must be a number")
        sys.exit(1)
    isFileResult = False
    if len(sys.argv) == 4:
        if not os.path.exists(sys.argv[3]):
            print("Error: file '%s' not found" % sys.argv[3])
        else:
            isFileResult = True
    if isFileResult:
        with open(sys.argv[3], 'r') as f:
            for line in f:
                if "Objective:  z =" in line:
                    result = line.split("Objective:  z = ")[1].split(" ")[0]
                    break
        print("Résultat de l'instance GLPK : %s" % result)
    else:
        result = -1
    actualTime = time.time()
    dict = parse(sys.argv[1])
    print("Temps de parsing : %f" % (time.time() - actualTime))
    isRunning = True
    # Main loop
    while(isRunning):
        print("1. Lancer l'algorithme glouton")
        print("2. Lancer l'algorithme Bron-Kerbosch")
        print("3. Lancer l'algorithme ACO")
        print("4. Lancer l'algorithme AG")
        print("5. Lancer tous les algorithmes à la suite")
        print("6. Quitter")
        choice = input("Choix : ")
        actualTime = time.time()
        if choice == "1":
            score = launchGlouton(dict)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
            if isFileResult:
                print(" Différence avec le résultat de l'instance GLPK : %d" % ((int(result) - score)/ int(result)))
        elif choice == "2":
            launchBronKerbosch(dict)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
        elif choice == "3":
            launchACO(dict, timeMax)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
        elif choice == "4":
            launchAG(dict, timeMax)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
        elif choice == "5":
            scoreGlouton = launchGlouton(dict)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
            scoreBronKerbosch = launchBronKerbosch(dict)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
            scoreaco = launchACO(dict, timeMax)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
            scoreAG = launchAG(dict, timeMax)
            print("Temps d'exécution : %f" % (time.time() - actualTime))
            if isFileResult:
                print("Résultat de l'instance GLPK : %s" % result)
            print("Score glouton : %d" % scoreGlouton)
            print("Score Bron-Kerbosch : %d" % scoreBronKerbosch)
            print("Score ACO : %d" % scoreaco)
            print("Score AG : %d" % scoreAG)
        elif choice == "6":
            isRunning = False
        else:
            print("Choix invalide")

def launchGlouton(dict):
    score = greedy.greedy(dict)
    print("Score : %d" % score)
    return score

def launchBronKerbosch(dict):
    max_clique = bk.find_all_cliques(possible_node_to_append_to_the_clique=parse(sys.argv[1]))
    # get max clique
    max_clique = max(max_clique, key=lambda x: sum([i.weight for i in x]))
    print([person.id for person in max_clique])
    score = sum([i.weight for i in max_clique])
    print("Poids de la clique : %d" % score)
    return score

def launchACO(dict, timeMax):
    clique, score = aco.aco(dict, timeMax)
    print("Score ACO : %d" % score)
    return score

def launchAG(dict, timeMax):
    score, list = ag.ag(dict, 0.8, 2/len(dict), 400, 100, 10000, timeMax)
    print("Score AG: %d" % score)
    return score, list

    
if __name__ == "__main__":
    main()
