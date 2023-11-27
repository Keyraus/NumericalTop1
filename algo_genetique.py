import glouton
import numpy as np

def intialisation_population(C, T):
    #initisalisation of the first solution with the glouton algorithm
    P = np.array([])

    for _ in range(T):
        #Add the solution to the population
        #random the C list
        P = np.append(P, glouton.glouton(C))
        np.random.shuffle(C)
       
    return P


    
