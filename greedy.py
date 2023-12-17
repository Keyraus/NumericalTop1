import numpy as np

def greedy(dict,gen = False, IsRandom = False):

    #dict is a dictionnary of Personne
    #gen is a boolean, if it's true, the function return the solution, if it's false, the function return the score
    #IsRandom is a boolean, if it's true, the function choose a random person to start with, if it's false, the function choose the person with the higher weight_heur

    list_persons = [i for i, _ in enumerate(dict)]
    #list persons is a list of the id of every persons in the dict
    S = [0 for _ in list_persons]
    #S is the solution, it's a list of 0 and 1, 1 if the person is invited, 0 otherwise

    max_weight = 0
    index = 0
    if IsRandom:
        #is the greedy is random, we choose a random person to start with
        index = np.random.randint(0, len(list_persons)) 
    else:
        #else we choose the person with the higher weight_heur
        for person in list_persons:
            if dict[person].weight_heur > max_weight:
                max_weight = dict[person].weight_heur
                index = person

    #we add the person to the solution and remove it from the list
    S[index] = 1
    list_persons.remove(index)

    #launch the heuristic until there is no more person to invite or until the heuristic return -1
    #the heuristic return -1 if nobody can fit in the solution
    while len(list_persons) > 0:
        i = heuristic(dict, S, False)
        if i == -1:
            break
        S[i] = 1
        list_persons.remove(i)

    score = 0

    #we calculate the score of the solution
    #the score is the sum of the weight of every person in the solution
    
    for i in np.nonzero(S)[0]:
        score += dict[i].weight
    #if gen is true, we return the solution, else we return the score
    if gen:
        return S
    else :
        return score


def heuristic(dict, S, random = False):
    #dict is a dictionnary of Personne
    #S is the solution, it's a list of 0 and 1, 1 if the person is invited, 0 otherwise
    #random is a boolean, if it's true, the function choose a random person to invite, if it's false, the function choose the person with the higher weight_heur

    if not random:
        max = -1 # might be a zero
        index = -1
        #we choose the first person in the solution to compare with the others
        first_pers_id = np.nonzero(S)[0][0]
        #we create a list of the id of every person in the solution
        all_ids = np.nonzero(S)[0]
        
        for person in np.nonzero(dict[first_pers_id].relations)[0]:
            #for every person in the relations of the first person
            value = dict[person].weight_heur * (not S[person])
            #we calculate the value of the person by multiplying his weight_heur by 1 if he is not already in the solution, 0 otherwise
            if value > max:
                #if the value is higher than the max, we check if the person can be invited
                for invited in all_ids:
                    if not dict[invited].relations[person]:
                        break
                else:
                    #if the person can be invited, we change the max and the index
                    max = value
                    index = person
        return index
    else:
        max = -1
        index = -1
        first_pers_id = np.nonzero(S)[0][0]
        proba_array = np.array([])
        people_array = np.array([])
        total = 0
        sumTotal = 0

            
        #for every person in the relations of the first person
        for person in dict[first_pers_id].relations:
            #if the person is already in the solution, we skip him
            if S[person] == 1:
                continue

            for invited in np.nonzero(S)[0]:
                if not dict[invited].is_friend(person):
                    break
            else:
                #if the person can be invited, we add him to the list of people that can be invited (people_array)
                #and we add his weight_heur * the number of relations he has (sumTotal)
                sumTotal += dict[person].weight * len(dict[person].relations)
                people_array = np.append(people_array, int(person))

        for people in dict[first_pers_id].relations:
            people = dict[int(people)] #people is a new an object Personne
            if people.id in people_array:
                #if the person can be invited, we calculate his probability to be invited (proba)
                proba = people.weight_heur / sumTotal
                #we add the probability to the array of probability (proba_array)
                proba_array = np.append(proba_array, total + proba)
                total += proba
            else:
                #if the person can't be invited, we add -1 to the array of probability (proba_array)
                proba_array = np.append(proba_array, -1)

        if len(proba_array) == 0 or len(people_array) == 0:
            #if there is no person that can be invited, we return -1
            return -1
        
        rand = np.random.random()
        person = 0
        for proba_1 in proba_array:
            if proba_1 > rand:
                break
            person += 1
        #we return the id of the person that has been chosen
        return dict[first_pers_id].relations[person].id
