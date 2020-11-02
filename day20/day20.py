from itertools import permutations
import re

if __name__ == "__main__":
    f = open("test1.txt", "r")
    regex = f.read().strip()
    print(regex)
    p = re.compile(regex)
    #m = p.match("ENWWWSSEN")
    groups = regex[1:-1]
    groups = groups.split("(")
    #groups = [r.split("|") for r in groups]
    #for r in groups:
    #    for i, c in enumerate(r):
    #        r[i] = c.strip(")")

    print(groups)
