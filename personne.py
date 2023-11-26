# This class is intended to store the information of a person
class Personne:
    def __init__(self, id, weight):
        self.id = int(id)
        self.weight = int(weight)
        self.relations = []
        self.invited = False

    def add_relation(self, relation):
        self.relations.append(relation)

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
