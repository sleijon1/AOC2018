""" this module solves day 2"""
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip


class Point:
    def __init__(self, x, y, edge=False):
        self.x = x
        self.y = y
        self.edge_point = edge
        self.closest_points = 0

    def __str__(self):
        return ("Point (" + str(self.x) + ", " + str(self.y) + ", " + \
                str(self.edge_point) + ")" +\
                " Amount of closest points: " + str(self.closest_points))

    def __repr__(self):
        return str(self)

    def set_edge_point(self):
        self.edge_point = True

    def manhattan_distance(self, point):
        """ Manhattan distance between instance and given point
        """
        diff_y = abs(self.y - point[1])
        diff_x = abs(self.x - point[0])
        return (diff_y + diff_x)

    def add_closest_point(self):
        self.closest_points += 1

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y
        )



def format_list(inp):
    """ formats the inp to list((int, int)) """
    formatted_list = []
    for value in inp:
        formatted_list.append(value.split(','))

    formatted_list = [(int(x[0]), int(x[1])) for x in formatted_list]
    return formatted_list

def max_values(points):
    """ Calculates the bounding values for the points

    Keyword args:
    points - list of integer double tuples
    """
    max_x = max([points[i][0] for i in range(len(points))])
    max_y = max([points[i][1] for i in range(len(points))])
    min_x = min([points[i][0] for i in range(len(points))])
    min_y = min([points[i][1] for i in range(len(points))])

    return max_x, max_y, min_x, min_y

def create_points(points):
    """ Creates Point objects out of list of points

    Keyword args:
    points - list of integer double tuples
    """
    point_list = []
    max_x, max_y, min_x, min_y = max_values(points)

    for point in points:
        x = point[0]
        y = point[1]

        new_point = Point(x, y)
        point_list.append(new_point)

    return point_list

def assign_points(points, point_list):
    """ Increments the points of point_list by the amount
    of points in points that are exclusively closest to them """
    max_x, max_y, min_x, min_y = max_values(points)

    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            # start with arbitrary point
            manhattan_list = []
            for point in point_list:
                manhattan_distance = point.manhattan_distance((x, y))
                manhattan_list.append((point, manhattan_distance))
                
            manhattan_list.sort(key=lambda x: x[1])
            closest_point = manhattan_list[0][0]
            # if distance still in the dict duplicate nodes
            # are equally close
            if manhattan_list[0][1] != manhattan_list[1][1]:
                if (x == max_x or x == min_x or y == min_y or y == max_y):
                    closest_point.set_edge_point()

                closest_point.add_closest_point()
        
    return point_list

def calculate_region(points, point_list):
    """ part2 - calculates the region where all points are less than
    10000 mhd away from all given points in point_list """
    max_x, max_y, min_x, min_y = max_values(points)
    safe_list = []
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            # start with arbitrary point
            total_distance = 0
            for point in point_list:
                manhattan_distance = point.manhattan_distance((x, y))
                total_distance += manhattan_distance
            if (total_distance < 10000):
                safe_list.append((x,y))
            
        
    return safe_list

def safest_point(point_list):
    """ Returns the non-edge point with most closest points """
    safest_point = None
    for point in point_list:
        if (point.edge_point is False \
            and (safest_point is None or \
                point.closest_points > safest_point.closest_points)):
            safest_point = point
    return safest_point

if __name__ == "__main__":
    input = read_and_strip()
    points = format_list(input)
    point_list = create_points(points)
    # assigns each given coordinate their amount of closest points
    assign_points(points, point_list)
    print("Part 1, safest point: " + str(safest_point(point_list)))
    print("Part 2: " + str(len(calculate_region(points, point_list))))
