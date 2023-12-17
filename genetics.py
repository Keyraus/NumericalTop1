# This file is intended to implement the genetic algoritm
# Librairies import
import greedy
import numpy as np
import time

# Function to initialize the population of the genetic algorithm
# Input: dict, the dictionnary of the problem
#        T, the size of the population
# Output: population, the population of the genetic algorithm
def init_population(dict, T):
    start = time.time()
    population = []
    # First solution is the greedy solution
    population.append(greedy.greedy(dict, True))
    for _ in range(T - 1):
        # All other solutions are random
        res = greedy.greedy(dict, True, True)
        population.append(res)
    #print("temps initialisation population : ", time.time() - start)
    return population

# Function to implement the genetic algorithm
# Input: dict, the dictionnary of the problem
#        hybridationProba, the probability of hybridation
#        mutationProba, the probability of mutation
#        T, the size of the population
#        T_used, the number of solutions used for the reproduction
#        IterMax, the maximum number of iterations
#        timeMax, the maximum time of execution
# Output: fbest, the best score found
#         population[np.argmax(scores)], the best solution found
def ag(dict, hybridationProba, mutationProba, T, T_used, IterMax, timeMax = 60):
    start = time.time()
    #print("Initialize population")
    population = init_population(dict, T)
    #print("Generated population : ", population")
    # init fbest
    fbest = 0
    
    #init a time delta
    for i in range(IterMax):
        #print("Iteration n°", i)
        # if time is up, stop
        if time.time() - start > timeMax:
            break
        # selection for reproduction
        M = selectionReproduction(dict, population, T_used)
        # hydridation and mutation and then reparation
        hybrids = createHybrids(M, hybridationProba)
        hybrids = mutation(hybrids, mutationProba)
        hybrids = reparation(dict, hybrids)
        population += hybrids
        fprimebest = 0

        scores = []
        # calculate the score of each solution
        for solution in population:
            #sum weight of each person in i
            nonzerosolution = np.nonzero(solution)[0]
            score = 0
            for people in nonzerosolution:
                score += dict[people].weight
            scores.append(score)
        #print("fbest : ", fbest, "fprimebest : ", fprimebest," temps : ", time.time() - start)
        if fprimebest > fbest:
            #print("new fbest : ", fprimebest)
            fbest = fprimebest
        #print(scores)
        # selection for survival
        population = selectForSurvival(dict, population, T)

    #print("nb iteration : ", i)
    return np.max(scores), population[np.argmax(scores)]

# Function to select the solutions for reproduction
# Input: dict, the dictionnary of the problem
#        population, the population of the genetic algorithm
#        T_used, the number of solutions used for the reproduction
# Output: M, the solutions selected for reproduction
def selectionReproduction(dict,population, T_used):
    M = []
    # calculate the score of each solution
    sumTotal = 0
    for solution in population:
        #sum wieght of each person in i
        score = 0
        nonzerosolution = np.nonzero(solution)[0]
        for people in nonzerosolution:
            score += dict[people].weight
        sumTotal += score

    # select T_used solutions based on their score and probability
    while len(M) < T_used:
        #calcul proba solution prise 
        solution = population[np.random.randint(0, len(population))]
        score_solution = 0
        nonzerosolution = np.nonzero(solution)[0]
        for people in nonzerosolution:
            score_solution += dict[people].weight
        proba_i = score_solution / sumTotal
        #calcul random pour savoir si solution prise ou pas 
        prise = np.random.randint(0, 1)
        if prise < proba_i:
            M.append(solution)
    return M

# Function to create the hybrids
# Input: M, the solutions selected for reproduction
#        hybridationProba, the probability of hybridation
# Output: Hybrids, the hybrids
def createHybrids(M, hybridationProba):
    hybrids = []
    # create hybrids
    while len(hybrids) < len(M):
        #taking a random int between 0 and 1 to know if we do a hybridation or not
        prise = np.random.randint(0, 1)
        i = M[np.random.randint(0, len(M))]
        j = M[np.random.randint(0, len(M))]
        # if prise < hybridationProba, we do a hybridation
        if prise < hybridationProba:
            # we take a random number of points to do the hybridation
            # we take random points in the solution
            point_hybrids = []
            for _ in range(np.random.randint(2,5)):
                point_hybrids.append(np.random.randint(0, len(i)))
            point_hybrids = sorted(point_hybrids)
            #print(point_hybrids)
            #print("i : ", i)
            #print("j : ", j)
            # get all the parts of i and j between the points of hybrids
            parted_i = np.split(i, point_hybrids)
            parted_j = np.split(j, point_hybrids)
            # put parts of i and j in i and j
            i = parted_i[0]
            j = parted_j[0]
            for index in range(1, len(parted_i)):
                if index % 2 == 0:
                    i = np.append(i, parted_i[index])
                    j = np.append(j, parted_j[index])
                else:
                    i = np.append(i, parted_j[index])
                    j = np.append(j, parted_i[index])
        
        hybrids.append(i)
        hybrids.append(j)

    return hybrids

# Function to do the mutation
# Input: hybrids, the hybrids
#        mutationProba, the probability of mutation
# Output: hybrids, the hybrids
def mutation(hybrids, mutationProba):
    len_solution = len(hybrids[0])
    # for each solution, we take a random number between 0 and 1
    # if the number is < mutationProba, we do a mutation
    for solution in hybrids:
        rand = np.random.default_rng().uniform(low=0.0, high=1.0, size=len_solution)
        for i,rnd in enumerate(rand):
            if rnd < mutationProba:
                #print(len(solution))
                solution[i] = 0 if solution[i] else 1
    return hybrids

# Function to do the reparation
# Input: dict, the dictionnary of the problem
#        hybrids, the hybrids
# Output: hybrids, the hybrids
def reparation(dict, hybrids):
    # calculate the repair score of each solution
    for solution in hybrids:
        repairTab = CalculScoreReparation(dict, solution)
    # if the solution is not valid, we repair it
        while np.sum(repairTab) > 0:
            min = float("inf")
            index = -1
            nonZeroTabRep = np.nonzero(repairTab)[0]
            for people in nonZeroTabRep:
                valeur = dict[people].weight_heur / repairTab[people]
                if valeur < min:
                    min = valeur
                    index = people
            solution[index] = 0
            repairTab = CalculScoreReparation(dict, solution)
    # after repair, we do a heuristic to improve the solution
    for solution in hybrids:
        if np.count_nonzero(np.array(solution)) == 0:
            continue
        index = -2
        while index != -1:
            index = greedy.heuristic(dict, solution)
            if index == -1:
                break
            solution[index] = 1
    return hybrids

# Function to calculate the repair score of each solution
# Input: dict, the dictionnary of the problem
#        solution, the solution
# Output: repairTab, the repair score of each solution
# This score is based on the number of people that doesn't know each other
def CalculScoreReparation(dict, solution):
    repairTab = [0 for _ in range(len(solution))]
    validSolutions = np.nonzero(solution)[0]
    for people in validSolutions:
        for people2 in validSolutions:
            if people != people2:
                if not dict[people].relations[people2]:
                    repairTab[people] += 1

    return repairTab


# Function to select the solutions for survival
# Input: dict, the dictionnary of the problem
#        population, the population of the genetic algorithm
#        T, the size of the population
# Output: population, the population of the genetic algorithm
def selectForSurvival(dict, population, T):
    # Creating a class to store the solution and its score
    class Solution:
        def __init__(self, solution, score):
            self.solution = solution
            self.score = score

    #create a list of with T entries and the score of each solution
    maxScore = []
    for sol_index in range(len(population)):
        #sum weight of each person in i
        score = 0
        for people in np.nonzero(population[sol_index])[0]:
            score += dict[people].weight
        #find the solution index in population
        maxScore.append(Solution(population[sol_index], score))
    
    maxScore = sorted(maxScore, key=lambda x: x.score, reverse=True)
    # keep the T best
    maxScore = maxScore[:T]

    # return the solution of the T best
    population = []
    for i in maxScore:
        population.append(i.solution)

    return population

# Function to calculate the diversity of the population
# Input: N, the number of people
#        T, the size of the population
#        population, the population of the genetic algorithm
#        prob_mutation, the probability of mutation
def calculDiversité(N, T, population, prob_mutation):
    diversité = 0
    for solutionI in population:
        for solutionJ in population:
            if np.array_equal(solutionI, solutionJ):
                continue
            diversité += np.sum(np.logical_xor(solutionI, solutionJ))
    diversité = diversité * 2 / (T * N * (T - 1))
    print("Diversité : ", diversité)
    if(diversité < 0.02):
        return prob_mutation  + 1/N
    return prob_mutation