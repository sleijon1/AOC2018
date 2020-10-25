import copy
import operator
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip
from collections import namedtuple

WATER = "|"
CLAY = "#"
SAND = "."
REST_WATER = "~"
LEFT = (-1, 0)
RIGHT = (1, 0)
DOWN = (0, 1)

def format_input(inp):
    """ formats input as [(static axis, val), (ranging axis, start, end)] """
    formatted = []
    for entry in inp:
        new_entry = []
        static, clay = entry.split(",")
        clay = clay.strip().split("..")
        x_y, start = clay[0].split("=")
        end = int(clay[1])
        static = static.split("=")
        static[1] = int(static[1])
        new_entry.append(tuple(static))
        new_entry.append((x_y, int(start), end))
        formatted.append(new_entry)
    #print(formatted)
    return formatted

def print_map(map_):
    for row in map_:
        string = ""
        for col in row:
            string = string + col
        print(string)

def create_map(inp):
    """ creates map from formatted input """
    all_x = []
    all_y = []
    for entry in inp:
        if entry[0][0] == 'x':
            all_x.append(entry[0][1])
            all_y.append(entry[1][2])
            all_y.append(entry[1][1])
        elif entry[0][0] == 'y':
            all_y.append(entry[0][1])
            all_x.append(entry[1][2])
            all_x.append(entry[1][1])

    map_ = []
    # water can flow on the side of the min and max x's
    min_x = min(all_x)-1
    max_x = max(all_x)+1
    min_y = 0
    for y in range(min_y, max(all_y)+1):
        row = []
        for x in range(min_x-1, max_x):
            row.append(".")
        map_.append(row)

    for clay in inp:
        if clay[0][0] == 'x':
            for y in range(clay[1][1], clay[1][2]+1):
                map_[y][clay[0][1]-min_x+1] = "#"
        elif clay[0][0] == 'y':
            for x in range(clay[1][1], clay[1][2]+1):
                map_[clay[0][1]][x-min_x+1] = "#"
    # water spring
    spring = (max_x-500, 0)
    map_[0][max_x-500] = "+"
    print_map(map_)
    return map_, spring


def propagate_water(map_, water):
    for unit in water:
        x = unit[0]
        y = unit[1]
        if map_[y+1][x] == SAND: # Go down
            map_[y+1][x] = WATER
            unit[1] = unit[1] + 1
        elif map_[y][x-1] == SAND: # Go left
            map_[y][x-1] = WATER
            unit[0] = unit[0] - 1
        elif map_[y][x+1] == SAND: # Go right
            map_[y][x+1] = WATER
            unit[0] = unit[0] + 1
        elif map_[y][x-1] == WATER  and map_[y+1][x-2] == SAND:
            unit[0] = unit[0] - 2
            unit[1] = unit[1] + 2
            map_[y+1][x-2] = WATER
        elif map_[y][x+1] == WATER  and map_[y+1][x+2] == SAND:
            unit[0] = unit[0] + 2
            unit[1] = unit[1] + 1
            map_[y+1][x+2] = WATER
        elif map_[y][x-1] == WATER  and map_[y][x-2] == SAND:
            unit[0] = unit[0] - 2
            map_[y][x-2] = WATER
        elif map_[y][x+1] == WATER  and map_[y][x+2] == SAND:
            unit[0] = unit[0] + 2
            map_[y][x+2] = WATER
        elif map_[y][x-1] in (CLAY, WATER) or map_[y][x+1] in (CLAY, WATER) and \
             map_[y][x-2] in (CLAY, WATER) or map_[y][x+2] in (CLAY, WATER):
            if  map_[y-1][x] == SAND:
                map_[y-1][x] = WATER
                unit[1] = unit[1] - 1
        map_[y][x] = SAND


def run_ticks(map_, spring, reps=47):
    start = [spring[0], spring[1]+1]
    water = list()
    map_[spring[1]+1][spring[0]] = WATER
    for i in range(reps):
        water.append(copy.deepcopy(start))
        print(water)
        print_map(map_)
        propagate_water(map_, water)

if __name__ == "__main__":
    inp = read_and_strip(file_name="test.txt")
    f_inp = format_input(inp)
    for n in f_inp:
        print(n)
    map_, spring = create_map(f_inp)
    run_ticks(map_, spring)
