# Usage : python3 convertion.py instance.txt instance.lp

import sys
import os
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
        # The objective function is the sum of the weights of the people invited
        for personne in personnes:
            f.write("+ %d x%d " % (personne.weight, personne.id))
        f.write("\n")
        # Write the constraints
        nb_constraints = 0
        f.write("Subject To\n")
        # This type of constraint : forall {j in 1..N, i in 1..N: i != j} (x[i] + x[j] <= 1) -> (i, j) out of E
        
        # Write the constraint for each person
        for person in personnes: 
            contraintePersonne = 0
            contraintesStr = ""
            # For each person, we check if he knows each other person
            for person2 in personnes:
                # We don't want to check twice the same relation
                if person.id < person2.id:
                    # If he not knows the person, we add the constraint
                    if not person.relations[person2.id]:
                        # We add the constraint
                        contraintePersonne += 1
                        contraintesStr += "+ x%d " % person2.id
            if contraintePersonne == 0:
                continue
            nb_constraints += 1
            contraintesStr = "    c%d: %d x%d %s  <= %d\n" % (nb_constraints,contraintePersonne, person.id, contraintesStr, contraintePersonne)
            f.write(contraintesStr)

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