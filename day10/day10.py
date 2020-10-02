import time
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip
from operator import add 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
#creating a subplot 
ax1 = fig.add_subplot(1,1,1)
#ax1.margins(0)

class LightPoints:
    """ class representing Santa's light guiding system """
    def __init__(self, points):
        self.points = points
        self.elapsed = 0

    def tick(self):
        self.elapsed += 1
        for point in self.points:
            point["pos"] = tuple(map(add, point["pos"], point["vel"]))
        return self.elapsed

    def positions(self):
        return [point["pos"] for point in self.points]

    def read(self):
        return self.points

def mh_distance(p1, p2):
    return (abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]))

def align_stars(points):
    while(True):
        all_aligned = True
        #print(points.positions())
        i = 0
        for point1 in points.positions():
            aligned_w_other = False
            for point2 in points.positions():
                if mh_distance(point1, point2) <= 2 and mh_distance(point1, point2) != 0 :
                    aligned_w_other = True
                    i += 1
                    # found one for which p1 aligns with
                    break
            if not aligned_w_other:
                all_aligned = False
                # some point have no alignment
                # we havent reached alignment
                break
        if not all_aligned:
            points.tick()
        else:
            break
    return points

def plot_graph(points):

    xs = []
    ys = []
    lines = points.positions()

    for line in lines:
        #print(line)
        x = line[0]
        y = line[1]*-1
        xs.append(float(x))
        ys.append(float(y))

    ax1.clear()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Live graph with matplotlib')

    plt.plot(xs, ys, linestyle='',marker='o')
    plt.show()

def format_input(points, scale=1, shift=0):
    formatted_points = []
    for point in points:
        pos_x = scale*int(point.split("<")[1].split(">")[0].split(',')[0])+shift
        pos_y = scale*int(point.split("<")[1].split(">")[0].split(',')[1])+shift
        position = (pos_x, pos_y)
        vel_x = int(point.split("<")[2].rstrip(">").split(",")[0])+shift
        vel_y = int(point.split("<")[2].rstrip(">").split(",")[1])+shift
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
    print(points)
    lightpoints = LightPoints(points)
    aligned_points = align_stars(lightpoints)
    print("Elapsed time: " + str(aligned_points.elapsed))
    plot_graph(aligned_points)


    #plt.show()

