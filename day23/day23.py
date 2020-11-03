import re
from copy import deepcopy
from math import sqrt
from z3 import *
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


""" z3 constraint solver comments:
  If(x,y,z) - if x then else z
  x = Int(x) - declare int x
  o.add(x == sum(y)) - for any solution
  x is the sum of y
"""
def z_mh_dist(x):
    """ mh distance formulated as z3 if """
    return If(x >= 0, x, -x)

# Decision Variables
(x, y, z) = (Int('x'), Int('y'), Int('z'))
dist_from_zero = Int('dist')
range_count = Int('sum')
in_ranges = [
    Int(str(i)) for i in range(len(data))
]

# We are trying to optimize
# amount of nanobots in range of a certain (x, y, z)
o = Optimize()

# Constraint
for i in range(len(data)):
    botx, boty, botz, botrange = data[i]
    # The i:th nanobot is in range of the (x, y, z)
    # coordinate iff the mh distance to (x, y, z)
    # is less or equal to its range
    o.add(in_ranges[i] == If(z_mh_dist(x-botx) + z_mh_dist(y-boty)
                             + z_mh_dist(z-botz) <= botrange, 1, 0))
# range_count is the sum of all nanobots in range
# of a (x, y, z)
o.add(range_count == sum(in_ranges))
# the distance to zero is the mh distance of a
# (x, y, z)
o.add(dist_from_zero == z_mh_dist(x) + z_mh_dist(y) + z_mh_dist(z))

# Objective Values
# Maximize the amount of nanobots
# in range to a (x, y, z) candidate solution
obj1 = o.maximize(range_count)
# Minimize the distance to (0, 0, 0) if more than one
# (x, y, z) candidate solution has the same
# amount of "in range" nanobots
obj2 = o.minimize(dist_from_zero)

print(o.check())
print("b", o.lower(obj2), o.upper(obj2))
