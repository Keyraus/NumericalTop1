# The program is intended to work with the following command line:
# python3 main.py temps input.txt output.txt
# where:
# - temps is the time in seconds the program has to run at the maximum
# - input.txt is the input file
# - output.txt is the output file
# The program will write the best solution found in the output file.
# Imports
import os
import sys
import time
from personne_parser import parse
from debuggerAlgorithms import launchAG
from bronkerbosch import find_all_cliques

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 main.py temps input.txt output.txt")
        sys.exit(1)
    # check if the instance file exists
    try:
        timeMax = int(sys.argv[1])
    except ValueError:
        print("Error: time must be a number")
        sys.exit(1)
    if not os.path.exists(sys.argv[2]):
        print("Error: file '%s' not found" % sys.argv[2])
        sys.exit(1)
    # check if the output file exists
    if os.path.exists(sys.argv[3]):
        print("Error: file '%s' already exists" % sys.argv[3])
        sys.exit(1)
    # parse the input file
    startTime = time.time()
    dict = parse(sys.argv[2])
    # launch the algorithm
    timeAfterParsing = time.time()
    # all_cliques = find_all_cliques(possible_node_to_append_to_the_clique=dict)
    # best_clique = max(all_cliques, key=lambda x: sum([i.weight for i in x]))
    # print([person.id for person in best_clique])
    # score = sum([i.weight for i in best_clique])
    # print("Poids de la clique : %d" % score)
    # print("Temps : ", time.time() - startTime)
    score, scoreArray = launchAG(dict, timeMax - (timeAfterParsing - startTime))
    print(scoreArray)
    line = ""
    for i in scoreArray:
        line += str(i) + " "
    print(line)
    # write in the file
    with open(sys.argv[3], 'w') as f:
        f.write(line)

if __name__ == "__main__":
    main()
