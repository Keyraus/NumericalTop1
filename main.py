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
    C = parse(sys.argv[1])
    print("Resulat attendu", result)
    score = glouton.glouton(C.copy())

    gap = (int(result) - score) / int(result)
    print("Gap : %f" % gap)

    # Run the genetic algorithm
    
    ag.ag(C.copy(), 0.8,2/len(C), 400, 100, 50)
if __name__ == "__main__":
    main()
