# Usage : python3 convertion.py instance.txt instance.lp

import sys
import os
from personne import Personne
from personne_parser import parse

def convertion(personnes, output):
    # We want to maximize the sum of the weights of the people invited
    # Each people must be invited at most once
    # Each people must know each other people invited
    # We will write this as a problem in LP format
    with open(output, 'a') as f:
        # We will use the GLPK solver
        # Write the objective function
        f.write("Maximize\n")
        f.write("    z: ")
        for personne in personnes:
            f.write("+ %d x%d " % (personne.weight, personne.id))
        f.write("\n")
        # Write the constraints
        nb_constraints = 0
        f.write("Subject To\n")
        # This type of constraint : forall {j in 1..N, i in 1..N: i != j} (x[i] + x[j] <= 1) -> (i, j) out of E
        for personne in personnes:
            for personne2 in personnes:
                if personne.id != personne2.id:
                    # We will write the constraint only if the two people are not friends
                    if not personne.is_friend(personne2):
                        if personne.id < personne2.id:
                            f.write("    c%d: x%d + x%d <= 1\n" % (nb_constraints, personne.id, personne2.id))
                            nb_constraints += 1

        # For the constraint we will write a c : at each new line
        # TODO
        # Write the binaries variables
        f.write("Binaries\n")
        for personne in personnes:
            f.write("    x%d\n" % personne.id)
        # Write the end of the file
        f.write("End\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 convertion.py instance.txt instance.lp")
        sys.exit(1)
    # check if the instance file exists
    if not os.path.exists(sys.argv[1]):
        print("Error: file '%s' not found" % sys.argv[1])
        sys.exit(1)
    instance = sys.argv[1]
    output = sys.argv[2]
    # create the output file
    if os.path.exists(output):
        # flush the content of the file
        open(output, 'w').close()
    # parse the instance file
    personnes = parse(instance)
    convertion(personnes, output)

main()
