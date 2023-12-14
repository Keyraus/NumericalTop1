import os

import glouton
import sys
import time
from personne_parser import parse
import algo_genetique as ag
import ant_colony_optimization as aoc
import copy
import numpy as np
import time
def main():
    start = time.time()
    if len(sys.argv) != 3:
        print("Usage: python3 main.py instance.txt instance.lp")
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
    # result = 1
    print("Résultat de l'instance GLPK : %s" % result)
    actualTime = time.time()
    # score = glouton.glouton(parse(sys.argv[1]))
    # print("Score : %d" % score)
    scores = []
    for i in range(5):
        clique, score2 = aoc.aoc(parse(sys.argv[1]))
        scores.append(score2)
        print("Score AOC : %d" % score2)
        # print the gap
        print("Gap : %f" % ((int(result) - score2) / int(result)))
        print("Temps d'exécution : %f" % (time.time() - actualTime))

    print("Minimum : ", np.min(scores))
    print("Moyenne : ", np.mean(scores))
    print("Maximum : ", np.max(scores))

    score = ag.ag(dict, 0.8, 2/len(dict), 400, 100, 500)
    print("Score AG: %d" % score )
    print("Gap : %.2f" % ((int(result) - score) / int(result)))
    
if __name__ == "__main__":
    main()
