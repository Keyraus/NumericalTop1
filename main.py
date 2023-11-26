import glouton
import os
import sys
from personne_parser import parse

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

if __name__ == "__main__":
    main()
