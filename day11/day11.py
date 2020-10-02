import sys
import numpy as np
sys.path.append("../")
from day1.day1part2 import read_and_strip

def cell_value(x, y, serial_number=1718):
    """ value function day 11 """
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    if len(str(power_level)) >= 3:
        power_level = int(str(power_level)[-3]) # get hundreds digit
    else:
        power_level = 0
    power_level -= 5
    return power_level

def largest_inner(matrix):
    """ returns the top-left coord of the
    largest inner matrix determined by adding cell value

    Keyword args:
    matrix -- the matrix to calculate
    """
    row = matrix.shape[0]
    col = matrix.shape[1]
    max_pl = 0
    last_coords = None
    for size in range(1, 300):
        print(size)
        for i in range(row):
            if i <= row-size:
                for k in range(col):
                    if k <= col-size:
                        power_level = 0
                        for j in range(i, i+size):
                            for l in range(k, k+size):
                                #print(j, l)
                                power_level += matrix[j, l]
                        if power_level > max_pl:
                            max_pl = power_level
                            last_coords = j-2, l-2
        print("max power lvl: " + str(max_pl) + ". coords: " + str(last_coords) +\
              " | size: " + str(size) + "x" + str(size))
    return max_pl, last_coords, size

def create_matrix(value_func=cell_value, col=300, row=300):
    """ Creates matrix with cell values determined by value_func

    Keyword args:
    value_func -- function to calculate values with
    """
    matrix = np.full((row, col), 0)
    assert(matrix.shape == (row, col))
    for i in range(row):
        for j in range(col):
            matrix[i,j] = value_func(i, j, 1718)
    return matrix

if __name__ == "__main__":
    value_matrix = create_matrix()
    assert(cell_value(3, 5, 8) == 4)
    max_pl, coords, size = largest_inner(value_matrix)
