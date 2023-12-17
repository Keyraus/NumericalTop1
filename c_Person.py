# This class is intended to store the information of a person
import numpy as np
# A person is defined by its id, its weight and its relations
class c_Person:
    def __init__(self, id, weight, len_dict):
        self.id = int(id)
        self.weight = int(weight)
        self.invited = False
        self.reparation = 0
        self.weight_heur = 0
        self.relations = [False for _ in range(len_dict)]

    def add_relation(self, c_Person):
        self.relations[c_Person.id] = True

    def calculate_weight_heur(self):
        self.weight_heur = self.weight * len(np.nonzero(self.relations)[0])

    def __str__(self):
        # display the person's id and weight and the list of relations
        string = "Personne %d (%d) (%d) : " % (self.id, self.weight, len(self.relations))
        for relation in self.relations:
            string += "%d " % relation
        return string

    def remove_relation(self, c_Person):
        for relation in self.relations:
            if relation.id == c_Person.id:
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