import sys
import os
import time
import numpy as np
from personne_parser import parse
import glouton
class Runner:

    def __init__(self):
        pass

    def glouton(self, Instance):
        score = glouton.glouton(Instance)
        print("Score : %d" % score)
        return glouton.glouton(Instance)
    
    def BronKerbosch(self, Instance):
        all_clique = glouton.find_all_cliques(possible_node_to_append_to_the_clique=parse(sys.argv[1]))
        print("Nombre de clique : %d" % len(all_clique))
        best_clique = max(all_clique, key=lambda x: sum([i.weight for i in x]))
        print([person.id for person in best_clique])
        score = sum([i.weight for i in best_clique])
        print("Poids de la clique : %d" % score)
        return score
    
    def BronKerboschOpti(self, Instance):
        max_clique = glouton.find_maximum_clique(possible_node_to_append_to_the_clique=parse(sys.argv[1]))
        print([person.id for person in max_clique])
        score = sum([i.weight for i in max_clique])
        print("Poids de la clique : %d" % score)
        return score