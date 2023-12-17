# Imports
import random
import numpy as np
import time

# Parameters used in ACO
pheromone_max = 20.0
pheromone_min = 0.1
pheromone_update = 0.1
pheromone_evaporation = 0.9
nb_ants = 100
cycle_max = 10000

# This method is used to initialize pheromones at the beginning of each cycle
# Input: personnes, the dictionnary of persons
# Output: initialzed pheromones list
def init_pheromones(personnes):
    return [pheromone_min for _ in range(0, len(personnes))]


# This method choose randomly a person among the dictionnary
# Input: personnes, the dictionnary of persons
# Output: a person chosen randomly
def select_random_vertex(personnes):
    return personnes[random.randint(0, len(personnes) - 1)]


# This method chose a person based on probabilities calculted thanks to pheromones
# Input: personnes, the dictionnary of persons
#        candidates, a list of candidate who can be append to the solution
#        pheromones, the current pheromones list 
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

# This method update the pheromones list
# Input: pheromones, the current pheromone list
#        clique, the current clique (solution)
# Ouput: pheromones, the current pheromone list
def update_pheromones(pheromones, clique):
    for vertex in clique:
        # Pheromone evaporation
        pheromones[vertex.id] *= pheromone_evaporation
        # Update the pheromone value based on its weight and relations lenght
        pheromones[vertex.id] += pheromone_update * vertex.weight * len(np.nonzero(vertex.relations))
        # Check the boundaries
        if pheromones[vertex.id] > pheromone_max:
            pheromones[vertex.id] = pheromone_max
        elif pheromones[vertex.id] < pheromone_min:
            pheromones[vertex.id] = pheromone_min
    return pheromones

# This method performs Ant Colony Optimization algorithm
# Input: personnes, the dictionnary of persons
#        timeMax, the maximum time used by the algorithm
# Output: the solution found and the score of its solution
def aco(personnes, timeMax = 60):

    # Initialize variables
    start = time.time()
    pheromones = init_pheromones(personnes)
    best_clique = []
    best_clique_score = 0

    # Perform algorithm {cycle_max} time
    for j in range(cycle_max):
        pheromones = init_pheromones(personnes)
        for ant in range(nb_ants):
            clique = []
            person = select_random_vertex(personnes)
            # print(person)
            clique.append(person)
            # All possibles candidates are person's relation
            candidates = [relation for relation in person.relations]
            # print(candidates)
            while len(np.nonzero(candidates)[0]) > 0:
                person = select_vertex_based_probabilities(personnes, candidates, pheromones)
                # print(person)
                clique.append(person)
                # Select possible candidates
                for i in range(len(candidates)):
                    if candidates[i] is True and person.relations[i] is True:
                        candidates[i] = True
                    else:
                        candidates[i] = False
            pheromones = update_pheromones(pheromones, clique)

            # Score calculation
            new_score = sum([vertex.weight for vertex in clique])
            if new_score > best_clique_score:
                # print(time.time() - start)
                # print("New Best Score found : ", new_score, "Itération n°", j, " => ", [p.id for p in clique])
                best_clique_score = new_score
                best_clique = clique
            if time.time() - start > timeMax:
                return best_clique, best_clique_score

    return best_clique, best_clique_score
