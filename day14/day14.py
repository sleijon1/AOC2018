from math import inf

class Elf:
    def __init__(self, i, recipe=None):
        self.current_recipe = recipe
        self.index = i
    def __str__(self):
        return str("Elf(" + str(self.current_recipe)+ ")")
    def __repr__(self):
        return str(self)

def produce_recipes(elfs, score_board, recipes=824501):
    while len(score_board) < recipes+10:
        recipe_sum = sum([elf.current_recipe for elf in elfs])
        for new_rec in str(recipe_sum):
            if len(score_board)+1 <= recipes+10:
                score_board.append(int(new_rec))
        for elf in elfs:
            step_forward = 1+elf.current_recipe
            if elf.index + step_forward > len(score_board)-1:
                recipe_index = (elf.index + step_forward) % len(score_board) # loop around
            else:
                recipe_index = elf.index + step_forward

            elf.current_recipe = score_board[recipe_index]
            elf.index = recipe_index
    return score_board[len(score_board)-10:len(score_board)+1]

def produce_recipes_two(elfs, score_board, score='824501'):
    i = 0
    while True:
        if len(score_board) >= len(score):
            score_ = "".join(map(str, score_board[i:i+len(score)]))
            if score_ == score:
                return i
            else:
                i += 1
        recipe_sum = sum([elf.current_recipe for elf in elfs])
        for new_rec in str(recipe_sum):
            score_board.append(int(new_rec))
        for elf in elfs:
            step_forward = 1+elf.current_recipe
            if elf.index + step_forward > len(score_board)-1:
                recipe_index = (elf.index + step_forward) % len(score_board) # loop around
            else:
                recipe_index = elf.index + step_forward

            elf.current_recipe = score_board[recipe_index]
            elf.index = recipe_index
    return None


def setup(score_board, no_elfs=2):
    elfs = []
    for i in range(no_elfs):
        new_elf = Elf(i, score_board[i])
        elfs.append(new_elf)
    return elfs

if __name__ == "__main__":
    # part one 
    #score_board=[3, 7]
    #elfs = setup(score_board)
    #last_ten = produce_recipes(elfs, score_board)
    #as_string = ''.join(map(str, last_ten))
    #print(score_board)
    #print(as_string)

    # part two
    score_board2=[3, 7]
    elfs2 = setup(score_board2)
    left_digits = produce_recipes_two(elfs2, score_board2)
    print("digits to the left: " + str(left_digits))
    #print("scoreboard2: " + str(score_board2))
