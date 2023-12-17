import glouton
import numpy as np
import time
from glouton import heuristicV2

def initialisation_population(dict, T):
    start = time.time()
    population = []
    population.append(glouton.gloutonV2(dict, True))
    for _ in range(T - 1):
        res = glouton.gloutonV2(dict, True, True)
        population.append(res)
    print("temps initialisation population : ", time.time() - start)
    return population

def ag(dict, ProbCroisement, ProbMutation, T, T_used, IterMax, timeMax = 60):
    start = time.time()
    #print("Génération de la population...")
    population = initialisation_population(dict, T)
    #print("Population générée, lancement...")
    #calculer le score de chaque individu 
    fbest = 0
    
    #init a time delta
    for i in range(IterMax):
        #print("Iteration n°", i)
        
        if time.time() - start > timeMax:
            break
        M = selectionReproduction(dict, population, T_used)
        Croisement = FuncCroisement(M, ProbCroisement)
        Croisement = Mutation(Croisement, ProbMutation)
        Croisement = ReparationV2(dict, Croisement)
        population += Croisement
        fprimebest = 0

        scores = []
        for solution in population:
            #sum wieght of each person in i
            nonzerosolution = np.nonzero(solution)[0]
            score = 0
            for personne in nonzerosolution:
                score += dict[personne].weight
            scores.append(score)
        #print("fbest : ", fbest, "fprimebest : ", fprimebest," temps : ", time.time() - start)
        if fprimebest > fbest:
            print("nouveau fbest : ", fprimebest)
            fbest = fprimebest
        #print(scores)
        population = selectionSurvie(dict, population, T)

    
    print("nb iteration : ", i)
    return np.max(scores), population[np.argmax(scores)]
# 9 16 162 197
def selectionReproduction(dict,population, T_used):
    M = []
    #calcul de la somme de tous les scores de la population
    sumTotal = 0
    for solution in population:
        #sum wieght of each person in i
        score = 0
        nonzerosolution = np.nonzero(solution)[0]
        for personne in nonzerosolution:
            score += dict[personne].weight
        sumTotal += score

    while len(M) < T_used:
        #calcul proba solution prise 
        solution = population[np.random.randint(0, len(population))]
        score_solution = 0
        nonzerosolution = np.nonzero(solution)[0]
        for personne in nonzerosolution:
            score_solution += dict[personne].weight
        proba_i = score_solution / sumTotal
        #calcul random pour savoir si solution prise ou pas 
        prise = np.random.randint(0, 1)
        if prise < proba_i:
            M.append(solution)
    return M

def FuncCroisement(M, ProbCroisement):
    Croisement = []
    while len(Croisement) < len(M):
        #calcul random pour savoir si solution prise ou pas 
        prise = np.random.randint(0, 1)
        i = M[np.random.randint(0, len(M))]
        j = M[np.random.randint(0, len(M))]
        if prise < ProbCroisement:
            point_croisement = []
            for _ in range(np.random.randint(2,5)):
                point_croisement.append(np.random.randint(0, len(i)))
            point_croisement = sorted(point_croisement)
            #print(point_croisement)
            #print("i : ", i)
            #print("j : ", j)
            # get all the parts of i and j between the points of croisement
            parted_i = np.split(i, point_croisement)
            parted_j = np.split(j, point_croisement)
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
        
        Croisement.append(i)
        Croisement.append(j)

    #print moyenne taille des solutions dans croisement

    return Croisement

def Mutation(Croisement, ProbMutation):
    len_solution = len(Croisement[0])
    for solution in Croisement:
        rand = np.random.default_rng().uniform(low=0.0, high=1.0, size=len_solution)
        for i,rnd in enumerate(rand):
            if rnd < ProbMutation:
                #print(len(solution))
                solution[i] = 0 if solution[i] else 1
    return Croisement

def Reparation(dict, Croisement): 
    #print("Réparation étape 1")
    for solution in Croisement:
        tableauReparation = CalculScoreReparation(dict, solution)
        while np.sum(tableauReparation) > 0:
            sommedesreparations = np.sum(tableauReparation)
            if(sommedesreparations == 0):
                break
            total = 0
            proba_array = np.array([])
            for personne in np.nonzero(tableauReparation)[0]:
                proba_1 = tableauReparation[personne] / dict[personne].weight_heur
                proba_array = np.append(proba_array, proba_1 + total)
                total += proba_1
            rand = np.random.random() * total
            personne = 0
            for proba_1 in proba_array:
                if proba_1 > rand:
                    break
                personne += 1
            personne = np.nonzero(tableauReparation)[0][personne]
            solution[personne] = 0
            tableauReparation[personne] = 0
    #print("Reparation étape 2")
    for solution in Croisement:
        if not np.sum(solution):
            continue
        index = -2
        while index != -1:
            index = heuristicV2(dict, solution)
            if index == -1:
                break
            solution[index] = 1

    return Croisement


def ReparationV2(dict, Croisement):
    #print("Réparation étape 1")
    for solution in Croisement:
        tableauReparation = CalculScoreReparation(dict, solution)

        while np.sum(tableauReparation) > 0:
            min = float("inf")
            index = -1
            nonZeroTabRep = np.nonzero(tableauReparation)[0]
            for personne in nonZeroTabRep:
                valeur = dict[personne].weight_heur / tableauReparation[personne]
                if valeur < min:
                    min = valeur
                    index = personne
            solution[index] = 0
            tableauReparation = CalculScoreReparation(dict, solution)
    #print("Reparation étape 2")
    for solution in Croisement:
        if np.count_nonzero(np.array(solution)) == 0:
            continue
        index = -2
        while index != -1:
            index = heuristicV2(dict, solution)
            if index == -1:
                break
            solution[index] = 1
    return Croisement


def CalculScoreReparation(dict, solution):
    tableauReparation = [0 for _ in range(len(solution))]
    validSolutions = np.nonzero(solution)[0]
    for personne in validSolutions:
        for personne2 in validSolutions:
            if personne != personne2:
                if not dict[personne].relations[personne2]:
                    tableauReparation[personne] += 1

    return tableauReparation



def selectionSurvie(dict, population, T):
    class Solution:
        def __init__(self, solution, score):
            self.solution = solution
            self.score = score

    #creer un tableau de score taille T
    maxScore = []
    for sol_index in range(len(population)):
        #sum wieght of each person in i
        score = 0
        for personne in np.nonzero(population[sol_index])[0]:
            score += dict[personne].weight
        #find the solution index in population
        maxScore.append(Solution(population[sol_index], score))
    
    maxScore = sorted(maxScore, key=lambda x: x.score, reverse=True)
    #garder les T meilleurs
    maxScore = maxScore[:T]

    #retourner les T meilleurs
    population = []
    for i in maxScore:
        population.append(i.solution)

    return population

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