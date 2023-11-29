import glouton
import numpy as np
import personne_parser as pp
import time

def initialisation_population(path, T):
    start = time.time()
    population = np.array([])
    population = np.append(population, glouton.gloutonGen(pp.parse(path)))
    for _ in range(T - 1):
        res = glouton.gloutonRandomGen(pp.parse(path))
        population = np.append(population, res).reshape(-1, len(res))
    print("temps initialisation population : ", time.time() - start)
    return population

def ag(C_init, ProbCroisement, ProbMutation, T, T_used, IterMax):
    population = initialisation_population(C_init, T)
    #calculer le score de chaque individu 
    fbest = 0
    for i in population:
        #sum wieght of each person in i
        score = 0
        for j in i:
            if j.invited:
                score += j.weight
        if score > fbest:
            fbest = score
    
    #commencement de la boucle
    print("debut de la boucle", fbest)
    #init a time delta
    start = time.time()

    for _ in range(IterMax):
        if time.time() - start > 120:
            break
        M = selectionReproduction(population, T_used)
        #print the mean invited people in each solution of M
        #list_invited = np.array([])
        #for i in M:
        #    invited = 0
        #    for j in i:
        #        if j.invited:
        #            invited += 1
        #    list_invited = np.append(list_invited, invited)
        #print("mean invited people in M : ", np.mean(list_invited))
        Croisement = FuncCroisement(M, ProbCroisement)
        #list_invited2 = np.array([])
        #for i in Croisement:
        #    invited = 0
        #    for j in i:
        #        if j.invited:
        #            invited += 1
        #    list_invited2 = np.append(list_invited2, invited)
        #print("mean invited people in croisement apres funcroisement : ", np.mean(list_invited2))
        Croisement = Mutation(Croisement, ProbMutation)
        #list_invited3 = np.array([])
        #for i in Croisement:
        #    invited = 0
        #    for j in i:
        #        if j.invited:
        #            invited += 1
        #    list_invited3 = np.append(list_invited3, invited)
        #print("mean invited people in croisement apres mutation : ", np.mean(list_invited3))
        Croisement = Reparation(Croisement)
        #list_invited4 = np.array([])
        #for i in Croisement:
        #    invited = 0
        #    for j in i:
        #        if j.invited:
        #            invited += 1
        #    list_invited4 = np.append(list_invited4, invited)
        #print("mean invited people in croisement apres reparation : ", np.mean(list_invited4))
        #print(len(Croisement), len(Croisement[0]))
        population = np.append(population, Croisement).reshape(-1, len(Croisement[0]))
        #print(len(population))
        #calculer le meilleur score de la population
        fprimebest = 0
        for i in population:
            #sum wieght of each person in i
            score = 0
            for j in i:
                if j.invited:
                    score += j.weight
            #print(score)
            if score > fprimebest: 
                fprimebest = score
                if fprimebest > 73:
                    print(fprimebest)

        print("fbest : ", fbest, "fprimebest : ", fprimebest," temps : ", time.time() - start)
        if fprimebest > fbest:
            print("nouveau fbest : ", fprimebest)
            fbest = fprimebest
        
        population = selectionSurvie(population, T)
   
    return fbest

def selectionReproduction(population, T_used):
    M = np.array([])
    #calcul de la somme de tous les scores de la population
    sumTotal = 0
    for i in population:
        #sum wieght of each person in i
        score = 0
        for j in i:
            score += j.weight
        sumTotal += score
    #selection de T_used individus
    while len(M) < T_used:
        #calcul proba solution prise 
        solution = population[np.random.randint(0, len(population))]
        score_i = 0
        for j in i:
            score_i += j.weight
        proba_i = score_i / sumTotal
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
        for personne in solution:
            randint = np.random.randint(0, 1)
            if randint < ProbMutation:
                personne.invited = not personne.invited

            
    return Croisement

def Reparation(Croisement): 
    for solution in Croisement:
        while isNotRealisable(solution):
            solution = CalculScoreReparation(solution)
            sommedesreparations = 0
            for personne in solution:
                sommedesreparations += personne.reparation
            if(sommedesreparations == 0):
                break
            for personne in solution:
                proba = personne.reparation / sommedesreparations
                randint = np.random.randint(0, 1)
                if randint < proba: #ptete pas bon
                    personne.invited = False
                    personne.reparation = 0

        for personne in solution:
            if not personne.invited:
                personne.invited = True
                for autreconnard in solution:
                    if autreconnard.invited:
                        if not personne.is_friend(autreconnard):
                            personne.invited = False
                            break
                    
    return Croisement


def CalculScoreReparation(solution):
    #faire un tableau numpy de gens invites
    invited = np.array([])
    for personne in solution:
        if personne.invited:
            invited = np.append(invited, personne)
    
    for convive in invited:
        for autreconnard in invited:
            if convive != autreconnard:
                if not convive.is_friend(autreconnard):
                    convive.reparation += 1

    return solution


def isNotRealisable(solution):
    for personne in solution:
        if not personne.invited:
            continue
        for connard in solution:
            if not connard.invited:
                continue
            if not personne.is_friend(connard):
                return True
    return False

def selectionSurvie(population, T):
    class Solution:
        def __init__(self, solution, score):
            self.solution = solution
            self.score = score

    #creer un tableau de score taille T
    maxScore = np.array([])
    for i in population:
        #sum wieght of each person in i
        score = 0
        for j in i:
            score += j.weight
        maxScore = np.append(maxScore, Solution(i, score))
    
    #trier le tableau
    #print(len(maxScore), maxScore[0])
    maxScore = sorted(maxScore, key=lambda x: x.score, reverse=True)
    #garder les T meilleurs
    maxScore = maxScore[:T]


    #retourner les T meilleurs
    population = np.array([])
    for i in maxScore:
        population = np.append(population, i.solution).reshape(-1, len(i.solution))    
   # print(len(population), len(population[0]))
    return population