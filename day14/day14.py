from math import inf

class Elf:
    def __init__(self, i, recipe=None):
        self.current_recipe = recipe
        self.index = i
    def __str__(self):
        return str("Elf(" + str(self.current_recipe)+ ")")
    def __repr__(self):
        return str(self)

def produce_recipes(elves, score_board, recipes=824501):
    """ Produces recipes amount of recipes+10 and returns the last 10 values """
    while len(score_board) < recipes+10:
        recipe_sum = sum([elf.current_recipe for elf in elves])
        for new_rec in str(recipe_sum):
            if len(score_board)+1 <= recipes+10:
                score_board.append(int(new_rec))
        for elf in elves:
            step_forward = 1+elf.current_recipe
            if elf.index + step_forward > len(score_board)-1:
                recipe_index = (elf.index + step_forward) % len(score_board) # loop around
            else:
                recipe_index = elf.index + step_forward

            elf.current_recipe = score_board[recipe_index]
            elf.index = recipe_index
    return score_board[len(score_board)-10:len(score_board)+1]

def produce_recipes_two(elves, score_board, score='824501'):
    """ Produces recipes until sequence score shows up on scoreboard
    returns the index of the first char in sequence
    """
    i = 0
    while True:
        if len(score_board) >= len(score):
            score_ = "".join(map(str, score_board[i:i+len(score)]))
            if score_ == score:
                return i
            else:
                i += 1
        recipe_sum = sum([elf.current_recipe for elf in elves])
        for new_rec in str(recipe_sum):
            score_board.append(int(new_rec))
        for elf in elves:
            step_forward = 1+elf.current_recipe
            if elf.index + step_forward > len(score_board)-1:
                recipe_index = (elf.index + step_forward) % len(score_board) # loop around
            else:
                recipe_index = elf.index + step_forward

            elf.current_recipe = score_board[recipe_index]
            elf.index = recipe_index
    return None


def setup(score_board, no_elves=2):
    """ creates no_elves amount of elves with score_board
    recipes and indices
    """
    elves = []
    for i in range(no_elves):
        new_elf = Elf(i, score_board[i])
        elves.append(new_elf)
    return elves

if __name__ == "__main__":
    # part one
    score_board=[3, 7]
    elves = setup(score_board)
    last_ten = produce_recipes(elves, score_board)
    as_string = ''.join(map(str, last_ten))
    print("last ten digits: " + as_string)

    # part two
    score_board2=[3, 7]
    elves2 = setup(score_board2)
    left_digits = produce_recipes_two(elves2, score_board2)
    print("digits to the left: " + str(left_digits))
