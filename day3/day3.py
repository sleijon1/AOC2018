""" this module solves day 3"""
import sys
sys.path.append("../")
import numpy
import itertools

from day1.day1part2 import read_and_strip

def split_information(rectangle):
    """splits rectangle formatted like: #1 @ 55,885: 22x10w
    and returns the x, y interval it ranges
    """

    rectangle = rectangle.split('@')[1].split(':')

    start_position = rectangle[0].split(',')
    start_x = int(start_position[0])
    start_y = int(start_position[1])

    end_position = rectangle[1].split('x')
    end_x = int(start_position[0])+int(end_position[0])
    end_y = int(start_position[1])+int(end_position[1])

    interval_x = range(start_x, end_x)
    interval_y = range(start_y, end_y)

    return interval_x, interval_y

def calculate_area_matrix(rectangles, bounding_x, bounding_y):
    """calculates the total area covered by at least two rectangles
    in rectangles

    Keyword arguments:
    rectangles -- list of #1 @ 55,885: 22x10w formatted rectangles
    bounding_x -- upper bound of x-coordinate
    bounding_y -- upper bound of y-coordinate
    """
    matrix = numpy.zeros((bounding_x, bounding_y))
    area = 0
    for rectangle in rectangles:
        ranges = split_information(rectangle)
        for i, j in itertools.product(ranges[0], ranges[1]):
            if matrix[i][j] == 1: # covered already
                matrix[i][j] = 2
                area += 1
            elif matrix[i][j] == 0: # havent covered yet
                matrix[i][j] = 1
    return matrix, area

def check_intact(matrix, ranges):
    """checks if the ranges are covered
    more than exactly once.
    """
    for i, j in itertools.product(ranges[0], ranges[1]):
        if matrix[i][j] == 2:
            return False
    return True

def find_intact_rectangle(rectangles, matrix):
    """finds if the rectangle in rectangles that is not
    covered by any other rectangle if there is one.
    """
    for rectangle in rectangles:
        ranges = split_information(rectangle)
        if check_intact(matrix, ranges):
            return rectangle
    return None

def run_day_three():
    """Run day three part 1 & 2 
    """
    inp = read_and_strip()
    area_matrix, area = calculate_area_matrix(inp, 1000, 1000)
    print(area_matrix, "\narea: " + str(area))
    print("\nintact rectangle without overlap: " + find_intact_rectangle(inp, area_matrix))
    
if __name__ == "__main__":
    run_day_three()
