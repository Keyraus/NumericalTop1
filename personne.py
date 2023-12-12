# This class is intended to store the information of a person
import numpy as np
class Personne:
    def __init__(self, id, weight, len_dict):
        self.id = int(id)
        self.weight = int(weight)
        self.invited = False
        self.reparation = 0
        self.weight_heur = 0
        self.relations = [False for _ in range(len_dict)]

    def add_relation(self, personne):
        self.relations[personne.id] = True
        self.weight_heur = self.weight * len(np.nonzero(self.relations)[0])


    def __str__(self):
        # display the person's id and weight and the list of relations
        string = "Personne %d (%d) (%d) : " % (self.id, self.weight, len(self.relations))
        for relation in self.relations:
            string += "%d " % relation
        return string

    def remove_relation(self, personne):
        for relation in self.relations:
            if relation.id == personne.id:
                self.relations.remove(relation)
                break
        return False
    
class relation:
    def __init__(self, id, weight):
        self.id = int(id)
        self.weight = int(weight)
    
    def __str__(self):
        return "Relation %d (%d)" % (self.id, self.weight)
    
    def __eq__(self, other):
        return self.id == other.id