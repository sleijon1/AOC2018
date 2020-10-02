import time
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip
from operator import add
import matplotlib.pyplot as plt

class DirectionalPoints:
    """ class representing x, y position and dx, dy velocity """
    def __init__(self, points):
        self.points = points
        self.elapsed = 0

    def tick(self):
        """ moves positions one step with their respective velocities """
        self.elapsed += 1
        for point in self.points:
            point["pos"] = tuple(map(add, point["pos"], point["vel"]))
        return self.elapsed

    def positions(self):
        """ returns all points positions """
        return [point["pos"] for point in self.points]

    def read(self):
        return self.points

def mh_distance(p1, p2):
    """ simple function for computing manhattan distance """
    return (abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]))

def align_points(points, distance=2):
    """ Elapses LightStars object points until they are aligned
    with a distance of distance
    Keyword args:
    points -- LightStars object to elapse
    distance -- Largest distance every point needs to have
    to at least one other point
    """
    while(True):
        all_aligned = True
        #print(points.positions())
        i = 0
        for point1 in points.positions():
            aligned_w_other = False
            for point2 in points.positions():
                if mh_distance(point1, point2) <= distance and mh_distance(point1, point2) != 0 :
                    aligned_w_other = True
                    i += 1
                    break
            if not aligned_w_other:
                all_aligned = False
                break
        if not all_aligned:
            points.tick()
        else:
            break
    return points

def plot_graph(points, show=False):
    """ Plots the current positions of the points
    Keyword args:
    points -- LightStars object of the stars to plot
    show -- True if plot graph
    """
    fig = plt.figure()
    # creating a subplot
    ax1 = fig.add_subplot(1,1,1)
    xs = []
    ys = []
    lines = points.positions()

    for line in lines:
        #print(line)
        x = line[0]
        y = line[1]*-1
        xs.append(float(x))
        ys.append(float(y))

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Live graph with matplotlib')

    plt.plot(xs, ys, linestyle='',marker='o')
    if show:
        plt.show()

def format_input(points):
    """ Formats point information to dict containing
    position and direction velocity """
    formatted_points = []
    for point in points:
        pos_x = int(point.split("<")[1].split(">")[0].split(',')[0])
        pos_y = int(point.split("<")[1].split(">")[0].split(',')[1])
        position = (pos_x, pos_y)
        vel_x = int(point.split("<")[2].rstrip(">").split(",")[0])
        vel_y = int(point.split("<")[2].rstrip(">").split(",")[1])
        velocity = (vel_x, vel_y)
        formatted_point = {}
        formatted_point["pos"] = position
        formatted_point["vel"] = velocity
        formatted_points.append(formatted_point)

    return formatted_points

if __name__ == "__main__":
    #inp = read_and_strip(file_name="small_input.txt")
    inp = read_and_strip(file_name="problem_input.txt")
    points = format_input(inp)
    lightpoints = DirectionalPoints(points)
    aligned_points = align_points(lightpoints)
    print("Elapsed time: " + str(aligned_points.elapsed))
    plot_graph(aligned_points, show=True)
