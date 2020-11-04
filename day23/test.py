import re
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



from z3 import *
def zabs(x):
  return If(x >= 0,x,-x)
(x, y, z) = (Int('x'), Int('y'), Int('z'))
in_ranges = [
  Int('in_range_' + str(i)) for i in range(len(data))
]
range_count = Int('sum')
o = Optimize()
for i in range(len(data)):
  nx, ny, nz, nrng = data[i]
  o.add(in_ranges[i] == If(zabs(x - nx) + zabs(y - ny) + zabs(z - nz) <= nrng, 1, 0))
o.add(range_count == sum(in_ranges))
dist_from_zero = Int('dist')
o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
h1 = o.maximize(range_count)
h2 = o.minimize(dist_from_zero)
print("test")
print (o.check())
#print o.lower(h1)
#print o.upper(h1)
print ("b", o.lower(h2), o.upper(h2))
#print o.model()[x]
#print o.model()[y]
#print o.model()[z]
