import re
from time import sleep

import numpy as np

mh_dist = lambda p1, p2: sum(abs(np.array(p1)-np.array(p2)))

f = open("test.txt").read().strip().splitlines()
INPUT = []
for line in f:
    x,y,z,f = map(int, re.findall(r"-?\d+", line))
    INPUT.append([x,y,z,f])

def calculate_constellations(inp):
    constellations = []
    for coord in inp:
        temp_constellations = []
        for constellation in constellations:
            for coord2 in constellation:
                if mh_dist(coord, coord2) <= 3:
                    temp_constellations.append(constellation)
                    break
        new_constellation = []
        if temp_constellations:
            for temp in temp_constellations:
                new_constellation += temp
                constellations.remove(temp)
        new_constellation.append(coord)
        constellations.append(new_constellation)
    print(constellations)
    print(len(constellations))

calculate_constellations(INPUT)
