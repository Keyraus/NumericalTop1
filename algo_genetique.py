import glouton
import numpy as np

def initialisation_population(C, T):
    population = np.array([])
    population = np.append(population, glouton.glouton(C))
    for i in range(T - 1):
        population = np.append(population, glouton.randomglouton(C))
    return population


def ag(C_init, ProbCroisement, ProbMutation, T, T_used, IterMax):
    population = initialisation_population(C_init, T)
    #calculer le score de chaque individu 
    fbest = 0
    for i in population:
        #sum wieght of each person in i
        score = 0
        for j in i:
            score += j.weight
        if score > fbest:
            fbest = score
    
    #commencement de la boucle

    for i in range(IterMax):
        M = selectionReproduction(population, T_used)
        Croisement = FuncCroisement(M, ProbCroisement)



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
        i = population[np.random.randint(0, len(population))]
        score_i = 0
        for j in i:
            score_i += j.weight
        proba_i = score_i / sumTotal
        #calcul random pour savoir si solution prise ou pas 
        prise = np.random.randint(0, 1)
        if prise < proba_i:
            M = np.append(M, population[i])
    return M

def FuncCroisement(M, ProbCroisement):
    Croisement = np.array([])
    while len(Croisement) < len(M):
        #calcul random pour savoir si solution prise ou pas 
        prise = np.random.randint(0, 1)
        i = M[np.random.randint(0, len(M))]
        j = M[np.random.randint(0, len(M))]
        if prise < ProbCroisement:
            point_i = int(len(i) / 2)
            point_j = int(len(j) / 2)

            i1 = i[:point_i]
            i2 = i[point_i:]
            j1 = j[:point_j]
            j2 = j[point_j:]

            i = np.append(i1, j2)
            j = np.append(j1, i2)

            Croisement = np.append(Croisement, i)
            Croisement = np.append(Croisement, j)
            
        else:
            Croisement = np.append(Croisement, i)
            Croisement = np.append(Croisement, j)
    
    return Croisement
