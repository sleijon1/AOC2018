class Elf:
    def __init__(self):
        self.current_recipe = None
    def set_recipe(self, recipe):
        self.current_recipe = recipe
    def __str__(self):
        return str("Elf(" + str(self.current_recipe)+ ")")
    def __repr__(self):
        return str(self)

def setup(no_elfs=2):
    score_board = [3, 7]
    problem_input = 824501
    elfs = []
    for _ in range(no_elfs):
        elfs.append(Elf())
    print(elfs)
    
if __name__ == "__main__":
    score_board = [3, 7]
    problem_input = 824501
    print(setup())
    
