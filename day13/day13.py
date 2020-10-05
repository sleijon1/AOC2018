import numpy as np
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

class Cart:
    """ Cart class adhering to specific movement rules """
    def __init__(self, x, y, direction):
        self.coordinates = {"x": x,
                            "y": y,
                            "dir":direction}
        self.x = x
        self.y = y
        self.direction = direction
        self.table = {
            (1, "v"):">",
            (1, "^"):"<",
            (1, ">"):"^",
            (1, "<"):"v",
            (2, "v"):"v",
            (2, "^"):"^",
            (2, ">"):">",
            (2, "<"):"<",
            (3, "v"):"<",
            (3, "^"):">",
            (3, ">"):"v",
            (3, "<"):"^",
        }
        self.turn = 1
        self.position = ""

    def take_turn(self):
        new_direction = self.table[(self.turn, self.direction)]
        if self.turn < 3:
            self.turn += 1
        elif self.turn == 3:
            self.turn = 1

        return new_direction

    def __str__(self):
        return "Cart: " + str((self.x, self.y, self.direction, self.position))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y and
            self.direction == other.direction
        )

    def move(self):
        if self.position == "+": # standing at intersection
            self.direction = self.take_turn()
        elif self.position == "/": # standing on curve
            if self.direction == "<":
                self.direction = "v"
            elif self.direction == "^":
                self.direction = ">"
            elif self.direction == ">":
                self.direction = "^"
            elif self.direction == "v":
                self.direction = "<"
        elif self.position == '\\': # standing on curve
            if self.direction == ">":
                self.direction = "v"
            elif self.direction == "^":
                self.direction = "<"
            elif self.direction == "v":
                self.direction = ">"
            elif self.direction == "<":
                self.direction = "^"

        if self.direction == '<':
            self.x -= 1
        elif self.direction == '>':
            self.x += 1
        elif self.direction == '^':
            self.y -= 1
        elif self.direction == 'v':
            self.y += 1

def print_map(map_):
    for row in map_:
        print("".join(row))

def tick(inp, carts):
    """ moves each cart once, returns position on collison otherwise None """
    updated = []
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
            if col == '<' or col == '>' \
               or col == '^' or col == 'v':
                check_cart = Cart(x, y, col)
                if (x, y) in updated:
                    continue
                if check_cart in carts:
                    cart = carts[carts.index(check_cart)]
                    cart.move() 
                    new_x = cart.x
                    new_y = cart.y
                    old_pos = cart.position
                    inp[y][x] = old_pos
                    if len([c for c in carts if c.x == new_x and c.y == new_y and c is not cart]) > 0:
                        print("Carts collided! They collided at: " + str((new_x, new_y)))
                        return (new_x, new_y)
                    else:
                        cart.position = inp[new_y][new_x]
                        inp[new_y][new_x] = cart.direction
                        updated.append((new_x, new_y))
                            
    return None


def create_carts(inp):
    """ creates list with carts in input """
    carts = []
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
            cart = None
            if col == '<' or col == '>':
                cart = Cart(x, y, col)
                cart.position = '-'
                carts.append(cart)
            elif col == '^' or col == 'v':
                cart = Cart(x, y, col)
                cart.position = '|'
                carts.append(cart)
    return carts

def tick_til_crash(inp):
    """ ticks all carts until collision happens"""
    for i in range(len(inp)):
        inp[i] = list(inp[i])
    carts = create_carts(inp)
    while(True):
        result = tick(inp, carts)
        if result is not None:
            inp[result[1]][result[0]] = "X"
            break
    return result

if __name__=="__main__":
    # small test
    f_test = open("test_input.txt", "r")
    test_inp = f_test.readlines()
    assert(tick_til_crash(test_inp) == (7, 3))

    # problem
    f = open("problem_input.txt", "r")
    inp = f.readlines()
    tick_til_crash(inp)
    #print(carts)
