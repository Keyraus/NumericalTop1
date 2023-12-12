import glouton
import numpy as np
import time
from glouton import heuristicV2

def initialisation_population(dict, T):
    start = time.time()
    population = []
    population.append(glouton.gloutonV2(dict, True, False))
    for _ in range(T - 1):
        res = glouton.gloutonV2(dict, True, True)
        population.append(res)
    print("temps initialisation population : ", time.time() - start)
    return population

def ag(dict, ProbCroisement, ProbMutation, T, T_used, IterMax):
    start = time.time()
    new_prob_mutation = ProbMutation
    #print("Génération de la population...")
    population = initialisation_population(dict, T)
    #print("Population générée, lancement...")
    #calculer le score de chaque individu 
    fbest = 0
    
    for solution in population:
        #sum wieght of each person in i
        score = 0
        for personne in np.nonzero(solution)[0]:
            score += dict[personne].weight
        if score > fbest:
            fbest = score
    
    #init a time delta
    for i in range(IterMax):
        #print("Iteration n°", i)
        
        if time.time() - start > 10:
            break
        M = selectionReproduction(dict, population, T_used)
        Croisement = FuncCroisement(M, ProbCroisement)
        
        Croisement = Mutation(Croisement, new_prob_mutation)
        Croisement = ReparationV2(dict, Croisement)
        population += Croisement
        fprimebest = 0

        scores = []
        for solution in population:
            nonzersolution = np.nonzero(solution)[0]
            score = 0
            for personne in nonzersolution:
                score += dict[personne].weight
            scores.append(score)

        if fprimebest > fbest:
            print("nouveau fbest : ", fprimebest)
            fbest = fprimebest

        population = selectionSurvie(dict, population, T)

    
    print("nb iteration : ", i)
    return np.max(scores)
# 9 16 162 197
def selectionReproduction(dict,population, T_used):
    M = []
    #calcul de la somme de tous les scores de la population
    sumTotal = 0
    for solution in population:
        #sum wieght of each person in i
        score = 0
        for personne in np.nonzero(solution)[0]:
            score += dict[personne].weight
        sumTotal += score

    while len(M) < T_used:
        #calcul proba solution prise 
        solution = population[np.random.randint(0, len(population))]
        score_solution = 0
        for personne in np.nonzero(solution)[0]:
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
            point_croisement = int(len(i) / 2)
            i1 = i[:point_croisement]
            i2 = i[point_croisement:]
            j1 = j[:point_croisement]
            j2 = j[point_croisement:]

            i1 = i1 + j2
            j1 = j1 + i2

        Croisement.append(i)
        Croisement.append(j)
        
    return Croisement

def Mutation(Croisement, ProbMutation):
    len_solution = len(Croisement[0])
    for solution in Croisement:
        rand = np.random.default_rng().uniform(low=0.0, high=1.0, size=len_solution)
        for i,rnd in enumerate(rand):
            if rnd < ProbMutation:
                solution[i] = not solution[i]
    return Croisement

def Reparation(dict, Croisement): 
    
    #print("Réparation étape 1")
    for solution in Croisement:
        while isNotRealisable(dict, solution):
            tableauReparation = CalculScoreReparation(dict, solution)
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
            solution[personne] = False
            tableauReparation[personne] = 0
    #print("Reparation étape 2")
    for solution in Croisement:
        if np.nonzero(solution)[0].size == 0:
            continue
        index = -2
        while index != -1:
            index = heuristicV2(dict, solution)
            if index == -1:
                break
            solution[index] = True

    return Croisement

# 
def ReparationV2(dict, Croisement): 

    #print("Réparation étape 1")
    for solution in Croisement:
        while isNotRealisable(dict, solution):
            tableauReparation = CalculScoreReparation(dict, solution)
            #glouton pour trouver la personne a enlever
            min = float("inf")
            index = -1
            for personne in np.nonzero(tableauReparation)[0]:
                valeur = dict[personne].weight_heur / tableauReparation[personne]
                if valeur < min:
                    min = valeur
                    index = personne
            solution[index] = False
            tableauReparation[index] = 0

    #print("Reparation étape 2")
    for solution in Croisement:
        if np.nonzero(solution)[0].size == 0:
            continue
        index = -2
        while index != -1:
            index = heuristicV2(dict, solution)
            if index == -1:
                break
            solution[index] = True
    return Croisement


def CalculScoreReparation(dict, solution):
    nonzerosolution = np.nonzero(solution)[0]
    tableauReparation = [0 for _ in range(len(solution))]
    for personne in nonzerosolution:
        for personne2 in nonzerosolution:
            if personne != personne2:
                if not dict[personne].relations[personne2]:
                    tableauReparation[personne] += 1

    return tableauReparation

def isNotRealisable(dict, solution):
    nonzerosolution = np.nonzero(solution)[0]
    for personne in nonzerosolution:
        for personne2 in nonzerosolution:
            if personne != personne2:
                if not dict[personne].relations[personne2]:
                    return True
    return False

def selectionSurvie(dict, population, T):
    class Solution:
        def __init__(self, solution, score):
            self.solution = solution
            self.score = score

    #creer un tableau de score taille T
    maxScore = []
    for sol_index in range(len(population)):
        nonzeropop = np.nonzero(population[sol_index])[0]
        #sum wieght of each person in i
        score = 0
        for personne in nonzeropop:
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
   # print(len(population), len(population[0]))
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