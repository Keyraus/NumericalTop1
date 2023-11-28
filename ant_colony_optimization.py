# Search of an approximate maximum clique in a graph G= (V, E ):
##############################################################################################################
# Initialize pheromone trails to τmaxrepeat the following cycle:
# for each ant kin 1..nbAnts, construct a maximal clique Ckas follows:
# Randomly choose a ﬁrst vertex vi∈V
# Ck← {vi}
# Candidates ← {vj∈V|(vi, vj)∈E}
# while Candidates 6=∅ do
# Choose a vertex vi∈
# Candidates with probability p(vi)
# Ck← Ck∪ {vi}
# Candidates ←Candidates ∩ {vj|(vi, vj)∈E}
# end
# while
# end for
# Update pheromone trails w.r.t. {C1,...,CnbAnts }
# if a pheromone trail is lower than τmin then set it to τmin
# if a pheromone trail is greater than τmax then set it to τmax
# until maximum number of cycles reached or optimal solution found
# return the largest constructed clique since the beginning
from random import random

pheromone_max = 1
pheromone_min = 0.0001
pheromone_update = 0.1
nb_ants = 10
cycle_max = 1000


def ant_colony_optimization(personnes):
    clique = []
    for i in range(cycle_max):
        for i in range(nb_ants):
            random_selected_vertex = select_first_vertex(personnes)
            clique.append(random_selected_vertex)
            candidates = random_selected_vertex.relations
            while len(candidates) != 0:
                chosen_vertex = choose_vertex_based_on_pheromones(candidates)
                clique.append(chosen_vertex)
                candidates = candidates.intersection(chosen_vertex.relations)
        update_pheromones(clique)
    return clique


def choose_vertex_based_on_pheromones(candidates):
    pass


def update_pheromones(clique):
    pass

def select_first_vertex(personnes):
    index = random.randint(0, len(personnes))
    return personnes[index]
















