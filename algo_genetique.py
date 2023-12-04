import glouton
import numpy as np
import time
from glouton import heuristicV2

def initialisation_population(dict, T):
    start = time.time()
    population = np.array([])
    population = np.append(population, glouton.gloutonV2(dict, True, False)).reshape(-1, len(dict))
    for _ in range(T - 1):
        res = glouton.gloutonV2(dict, True, True)
        population = np.append(population, res).reshape(-1, len(res))
    print("temps initialisation population : ", time.time() - start)
    return population

def ag(dict, ProbCroisement, ProbMutation, T, T_used, IterMax):
    population = initialisation_population(dict, T)
    #calculer le score de chaque individu 
    fbest = 0
    
    for solution in population:
        #sum wieght of each person in i
        score = 0
        for personne in np.nonzero(solution)[0]:
            score += dict[personne].weight
        if score > fbest:
            fbest = score
    
    #commencement de la boucle
    print("debut de la boucle", fbest)
    #init a time delta
    start = time.time()

    for _ in range(IterMax):
        if time.time() - start > 200:
            break
        M = selectionReproduction(dict, population, T_used)
        Croisement = FuncCroisement(M, ProbCroisement)
        Croisement = Mutation(Croisement, ProbMutation)
        Croisement = Reparation(dict, Croisement)
        population = np.append(population, Croisement).reshape(-1, len(Croisement[0]))
        fprimebest = 0

        for solution in population:
            #sum wieght of each person in i
            score = 0
            for personne in np.nonzero(solution)[0]:
                score += dict[personne].weight
            
            if score > fprimebest: 
                fprimebest = score
                if fprimebest > 73:
                    print("wtf pas possible", fprimebest)

        #print("fbest : ", fbest, "fprimebest : ", fprimebest," temps : ", time.time() - start)
        if fprimebest > fbest:
            print("nouveau fbest : ", fprimebest)
            fbest = fprimebest
        
        population = selectionSurvie(dict, population, T)
   
    return fbest
# 9 16 162 197
def selectionReproduction(dict,population, T_used):
    M = np.array([])
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
            M = np.append(M,solution).reshape(-1, len(solution))
    return M

def FuncCroisement(M, ProbCroisement):
    Croisement = np.array([])
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

            i = np.append(i1, j2)
            j = np.append(j1, i2)

        Croisement = np.append(Croisement, i).reshape(-1, len(i))
        Croisement = np.append(Croisement, j).reshape(-1, len(j))
        
    
    return Croisement

def Mutation(Croisement, ProbMutation):
    for solution in Croisement:
        for i in range(len(solution)):
            rand = np.random.random() % 1
            if rand < ProbMutation:
                solution[i] = not solution[i]
    return Croisement

def Reparation(dict, Croisement): 
    print("Réparation étape 1")
    for solution in Croisement:
        while isNotRealisable(dict, solution):
            tableauReparation = CalculScoreReparation(dict, solution)
            # print(np.nonzero(tableauReparation)[0])
            # print(len(np.nonzero(tableauReparation)[0]))
            # print(tableauReparation)
            sommedesreparations = np.sum(tableauReparation)
            # print(sommedesreparations)
            # input()
            if(sommedesreparations == 0):
                break
            total = 0
            # calculate proba in interval [0,1] to remove a person
            proba_array = np.array([])
            for personne in np.nonzero(tableauReparation)[0]:
                #proba_1 = tableauReparation[personne] / sommedesreparations
                proba_1 = tableauReparation[personne] / dict[personne].weight_heur
                # put interval in array from 0 to 1
                proba_array = np.append(proba_array, proba_1 + total)
                total += proba_1
            #find the person position in the solution
            rand = np.random.random() * total
            #print("rand : ", rand)
            #print("proba_array : ", proba_array)
            personne = 0
            for proba_1 in proba_array:
                if proba_1 > rand:
                    break
                personne += 1
            # print("rand : ", rand)
            # print("proba_array : ", proba_array)
            # print(proba_array[personne])
            # print("personne : ", personne)
            personne = np.nonzero(tableauReparation)[0][personne]
            # print("personne : ", personne)
            #remove the person from the solution
            #print("personne : ", personne)
            #print("solution avant : ", solution)
            solution[personne] = False
            #print("solution apres : ", solution)
            tableauReparation[personne] = 0
            #print("tableauReparation apres : ", tableauReparation)
    print("Reparation étape 2")
    for solution in Croisement:
        if solution[8] and solution[15]:
            print("solution contient 8 et 15")
            print(solution)
           # input()
        if np.nonzero(solution)[0].size == 0:
            continue
        index = -2
        while index != -1:
            index = heuristicV2(dict, solution)
            if index == -1:
                break
            solution[index] = True
   # print("Fin de la réparation")
   # print(Croisement[0])
    #print(np.nonzero(Croisement[0])[0])
   # print(len(np.nonzero(Croisement[0])[0]))
   # input()
    return Croisement


def CalculScoreReparation(dict, solution):
    tableauReparation = [0 for _ in range(len(solution))]
    for personne in np.nonzero(solution)[0]:
        for personne2 in np.nonzero(solution)[0]:
            if personne != personne2:
                if not dict[personne].is_friend(dict[personne2]):
                    tableauReparation[personne] += 1

    return tableauReparation

def isNotRealisable(dict, solution):
    for personne in np.nonzero(solution)[0]:
        for personne2 in np.nonzero(solution)[0]:
            if personne != personne2:
                if not dict[personne].is_friend(dict[personne2]):
                    return True
    return False

def selectionSurvie(dict, population, T):
    class Solution:
        def __init__(self, solution, score):
            self.solution = solution
            self.score = score

    #creer un tableau de score taille T
    maxScore = np.array([])
    for sol_index in range(len(population)):
        #sum wieght of each person in i
        score = 0
        for personne in np.nonzero(population[sol_index])[0]:
            score += dict[personne].weight
        #find the solution index in population
        maxScore = np.append(maxScore, Solution(population[sol_index], score))
    
    maxScore = sorted(maxScore, key=lambda x: x.score, reverse=True)
    #garder les T meilleurs
    maxScore = maxScore[:T]

    #retourner les T meilleurs
    population = np.array([])
    for i in maxScore:
        population = np.append(population, i.solution).reshape(-1, len(i.solution))    
   # print(len(population), len(population[0]))
    return population