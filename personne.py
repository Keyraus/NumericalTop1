# This class is intended to store the information of a person
class Personne:
    def __init__(self, id, weight):
        self.id = int(id)
        self.weight = int(weight)
        self.relations = []
        self.invited = False
        self.reparation = 0
        self.weight_heur = 0

    def add_relation(self, personne):
        rel = relation(personne.id, personne.weight)
        self.relations.append(rel)
        self.weight_heur = self.weight * len(self.relations)


    def __str__(self):
        # display the person's id and weight and the list of relations
        string = "Personne %d (%d) (%d) : " % (self.id, self.weight, len(self.relations))
        for relation in self.relations:
            string += "%d " % relation.id
        return string
    
    def is_friend(self, personne):
        for relation in self.relations:
            if relation.id == personne.id:
                return True
        return False
    
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