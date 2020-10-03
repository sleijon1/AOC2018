import numpy as np
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip


def create_matrix(inp):
    largest_x = max([len(entry) for entry in inp])
    largest_y = len(inp)
    print(inp)

if __name__=="__main__":
    # TODO: new read function need whitespace
    inp = read_and_strip(file_name="test_input.txt")
    print(inp)
    create_matrix(inp)
