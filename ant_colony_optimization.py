# Search of an approximate maximum clique in a graph G= (V, E ):
##############################################################################################################
# Initialize pheromone trails to τmax repeat the following cycle:
# for each ant kin 1..nbAnts, construct a maximal clique Ckas follows:
# Randomly choose a first vertex vi∈V
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
import random
import numpy as np
import time

pheromone_max = 20.0
pheromone_min = 0.1
pheromone_update = 0.1
pheromone_evaporation = 0.9
nb_ants = 100
cycle_max = 10000


def init_pheromones(personnes):
    return [pheromone_min for _ in range(0, len(personnes))]


def select_random_vertex(personnes):
    return personnes[random.randint(0, len(personnes) - 1)]


def select_vertex_based_probabilities(personnes, candidates, pheromones):
    # print("Candidate : ", candidates)
    relation_indexes = np.nonzero(candidates)[0]
    # print(relation_indexes)
    sum_pheromones = round(sum([pheromones[index] for index in relation_indexes]), 2)
    # print(len(relation_indexes))
    # print(sum_pheromones)
    probabilities = [pheromones[index] / sum_pheromones for index in relation_indexes]
    # print(len(probabilities), probabilities)
    return personnes[random.choices(relation_indexes, probabilities)[0]]


def update_pheromones(pheromones, clique):
    for vertex in clique:
        pheromones[vertex.id] *= pheromone_evaporation
        pheromones[vertex.id] += pheromone_update * vertex.weight * len(np.nonzero(vertex.relations))
        if pheromones[vertex.id] > pheromone_max:
            pheromones[vertex.id] = pheromone_max
        elif pheromones[vertex.id] < pheromone_min:
            pheromones[vertex.id] = pheromone_min
    return pheromones


def aoc(personnes, timeMax = 60):
    start = time.time()
    pheromones = init_pheromones(personnes)
    best_clique = []
    best_clique_score = 0
    # print(pheromones, len(pheromones))
    for j in range(cycle_max):
        pheromones = init_pheromones(personnes)
        for ant in range(nb_ants):
            clique = []
            person = select_random_vertex(personnes)
            # print(person)
            clique.append(person)
            candidates = [relation for relation in person.relations]
            # print(candidates)
            while len(np.nonzero(candidates)[0]) > 0:
                person = select_vertex_based_probabilities(personnes, candidates, pheromones)
                # print(person)
                clique.append(person)
                # print("C Before", candidates)
                # print("R Before", person.relations)
                for i in range(len(candidates)):
                    if candidates[i] is True and person.relations[i] is True:
                        candidates[i] = True
                        # print(i)
                    else:
                        candidates[i] = False
                # print("C After", candidates)
            pheromones = update_pheromones(pheromones, clique)

            new_score = sum([vertex.weight for vertex in clique])
            if new_score > best_clique_score:
                print(time.time() - start)
                print("New Best Score found : ", new_score, "Itération n°", j, " => ", [p.id for p in clique])
                best_clique_score = new_score
                best_clique = clique
            if time.time() - start > timeMax:
                return best_clique, best_clique_score

    return best_clique, best_clique_score
