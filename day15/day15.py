class Player:
    """ parent class player """
    def __init__(self):
        """ hp = hit points, ap = attack power """
        
        self.hp = 200
        self.ap = 3
    
class Elf(Player):
    def __str__(self):
        return "Elf(hp:" + str(self.hp) + ", ap:" + str(self.ap) + ")"
    def __repr__(self):
        return str(self)
    pass

class Goblin(Player):
    def __str__(self):
        return "Goblin(hp:" + str(self.hp) + ", ap:" + str(self.ap) + ")"
    def __repr__(self):
        return str(self)
    pass

if __name__ == "__main__":
    elf = Elf()
    goblin = Goblin()
    print((elf, goblin))
 
