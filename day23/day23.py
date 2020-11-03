import re
from copy import deepcopy
from math import sqrt

import numpy as np

data = []
for line in open("input.txt").read().splitlines():
    a, b, c, d = map(int, re.findall(r'-?\d+', line))
    data.append([a, b, c, d])

mh_dist = lambda p1, p2: sum(abs(np.array(p1)-np.array(p2)))
most_powerful = [max(data, key=lambda bot: bot[3]), 0]
distances = np.array([mh_dist(most_powerful[0][0:3], bot[0:3]) for bot in data])

print("Number of in range drones: " + str(sum(distances <= most_powerful[0][3])) + \
      " of master drone: " + str(most_powerful[0]))

min_x = min([bot[0] for bot in data])
min_y = min([bot[1] for bot in data])
min_z = min([bot[2] for bot in data])

max_x = max([bot[0] for bot in data])
max_y = max([bot[1] for bot in data])
max_z = max([bot[2] for bot in data])
min_xyz = [min_x, min_y, min_z]
max_xyz = [max_x, max_y, max_z]

coords = {
}
print(min_xyz, max_xyz)
for i in range(min_x, max_x+1):
    for j in range(min_y, max_y+1):
        for k in range(min_z, max_z+1):
            for bot in data:
                if mh_dist((i,j,k), bot[0:3]) <= bot[3]:
                    try:
                        coords[(i,j,k)] += 1
                    except KeyError:
                        coords[(i,j,k)] = 1
print(max(coords.values()))
