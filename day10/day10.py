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

class LightPoints:
    """ class representing Santa's light guiding system """
    def __init__(self, points):
        self.points = points

    def tick(self):
        for point in self.points:
            point["pos"] = tuple(map(add, point["pos"], point["vel"]))

    def positions(self):
        return [point["pos"] for point in self.points]

    def read(self):
        return self.points

def animate(_, points):
    data = open('stock.txt','r').read()
    #lines = data.split('\n')
    #lines.pop(-1)

    xs = []
    ys = []
    lines = points.positions()
    print(lines)
    for line in lines:
        #x, y = line.split(',') # Delimiter is comma
        x = line[0]
        y = line[1]
        xs.append(float(x))
        ys.append(float(y))

    ax1.clear()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Live graph with matplotlib')
    plt.scatter(xs, ys)
    points.tick()

def format_input(points):
    formatted_points = []
    for point in points:
        pos_x = int(point[10:12])
        pos_y = int(point[14:16])
        position = (pos_x, pos_y)
        vel_x = int(point[28:30])
        vel_y = int(point[32:34])
        velocity = (vel_x, vel_y)
        #print(velocity)
        formatted_point = {}
        formatted_point["pos"] = position
        formatted_point["vel"] = velocity
        formatted_points.append(formatted_point)

    return formatted_points

if __name__ == "__main__":
    inp = read_and_strip(file_name="small_input.txt")
    points = format_input(inp)
    lightpoints = LightPoints(points)
    ani = animation.FuncAnimation(fig, animate, fargs=(lightpoints, ), interval=200)
    plt.show()

