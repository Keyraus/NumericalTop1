import glouton
import sys
from personne_parser import parse
import algo_genetique as ag
import copy
import numpy as np
def main():
    with open(sys.argv[2], 'r') as f:
        for line in f:
            if "Objective:  z =" in line:
                result = line.split("Objective:  z = ")[1].split(" ")[0]
                break
    # Print the result
    dict = parse(sys.argv[1])

    print("Resulat attendu", result)

    stest = glouton.gloutonV2(dict, 0, 1)
    print(np.nonzero(stest)[0])
    #print all the raltions of 15 with their wieght
    #print("Score glouton : %d" % score )
    #gap = (int(result) - score) / int(result)
    #print("Score glouton : %d" % score )
    #print("Gap : %f" % gap)


    score = ag.ag(dict, 0.8, 0.2, 400, 100, 500)
    print("Score AG: %d" % score )


    
if __name__ == "__main__":
    main()
