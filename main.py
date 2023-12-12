import glouton
import sys
from personne_parser import parse
import algo_genetique as ag
import copy
import numpy as np
import time
def main():
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if "Objective:  z =" in line:
                result = line.split("Objective:  z = ")[1].split(" ")[0]
                break
    # Print the result
    dict = parse(sys.argv[1])

    print("Resulat attendu", result)
    for _ in range(5):
        start = time.time()
        score = glouton.glouton(dict)
        end = time.time()
        print("Score glouton : %d" % score, "Time : %.2f" % (end - start) )
        print("Gap : %.2f" % ((int(result) - score) / int(result)))


        score = ag.ag(dict, 0.8, 2/len(dict), 400, 100, 500)
        print("Score AG: %d" % score )
        print("Gap : %.2f" % ((int(result) - score) / int(result)))
    
if __name__ == "__main__":
    main()
