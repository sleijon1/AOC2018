import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip
from typing import List
from copy import deepcopy

TREES = "|"
YARD = "#"
OPEN = "."

def print_map(map_):
    """ prints rows of lists as strings for compact
    representation and newlines """
    for row in map_:
        string = ""
        for col in row:
            string = string + col
        print(string)

def adjacent(grid, x, y) -> List[str]:
    """ returns (x, y)'s adjacent values """
    adj = []
    dirs = [(x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1),
            (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1)]
    adj = [grid[row][col] for col, row in dirs if row >= 0 and row < len(grid)
           and col >= 0 and col < len(grid[0])]
    return adj

def elapse(grid, times):
    """ elapses times amount """
    for minute in range(times):
        temp = deepcopy(grid)
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                adj = adjacent(grid, x, y)
                if col == OPEN and adj.count(TREES) >= 3:
                    temp[y][x] = TREES
                elif col == TREES and adj.count(YARD) >= 3:
                    temp[y][x] = YARD
                if col == YARD:
                    if adj.count(YARD) >= 1 and adj.count(TREES) >= 1:
                        temp[y][x] = YARD  # redundant
                    else:
                        temp[y][x] = OPEN
        grid = temp
        print("After " + str(minute+1) + " minutes.")
        print_map(grid)
    return grid


if __name__ == "__main__":
    INPUT = read_and_strip(file_name="input.txt")
    grid = [list(row) for row in INPUT]
    print_map(grid)
    print(adjacent(INPUT, 9, 9))
    last_grid = elapse(grid, 1000)  # repeats pattern after a few hundred times
    resource_value = sum([row.count(TREES) for row in last_grid]) * \
        sum([row.count(YARD) for row in last_grid])
    print("Resource value (trees*yard) = " + str(resource_value))
