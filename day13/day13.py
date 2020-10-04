import numpy as np
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

class Cart:
    def __init__(self, x, y, direction):
        self.coordinates = {"x": x,
                            "y": y,
                            "dir":direction}
        self.x = x
        self.y = y
        self.direction = direction
        self.table = {
            1:"<",
            2:self.direction,
            3:">",
        }
        self.turn = 1
        self.position = ""

    def take_turn(self):
        take = turn
        if self.turn < 3:
            self.turn += 1
        return take[take]

    def __str__(self):
        return "Cart: " + str((self.x, self.y, self.direction))

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
            elif self.direction == "v":
                self.direction = "<"
        elif self.position == '\\': # standing on curve
            if self.direction == ">":
                self.direction = "v"
            elif self.direction == "^":
                self.direction = "<"
            elif self.direction == "v":
                self.direction = ">"

        if self.direction == '<':
            self.x -= 1
        elif self.direction == '>':
            self.x += 1
        elif self.direction == '^':
            self.y -= 1
        elif direction == 'v':
            self.y += 1

def cart_predicate(line):
    """ returns true if cart exists and its index"""
    for element in line:
        if element == '<' or element == '>' \
           or element == '^' or element == 'v':
            return True, line.index(element)

def tick(inp, carts):
    for y, row in enumerate(inp):
        #print(inp)
        for x, col in enumerate(row):
            if col == '<' or col == '>' \
               or col == '^' or col == 'v':
                check_cart = Cart(x, y, col)
                print(carts)
                print(check_cart)
                if check_cart in carts:
                    print("XD")
                    cart = carts[carts.index(check_cart)]
                    # need to check if cart is on crossroads or curve
                    cart.move() # tick current cart
                    new_x = cart.x
                    new_y = cart.y
                    old_pos = cart.position
                    cart.position = inp[new_y][new_x]
                    inp[y][x] = old_pos
                    crashes = [(x, y) for cart in carts if \
                             cart.x == new_x and cart.y == new_y]
                    if len(crashes) > 0:
                        return crashes
    return None


def create_carts(inp):
    """ creates list with carts in input """
    carts = []
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
            cart = None
            if col == '<' or col == '>' \
               or col == '^' or col == 'v':
                cart = Cart(x, y, col)
                carts.append(cart)
    return carts

if __name__=="__main__":
    inp = read_and_strip(file_name="test_input.txt")
    carts = create_carts(inp)
    while(True):
        result = tick(inp, carts)
        if result is not None:
            print("wooga")
            break
    print(result)

    print(carts)
