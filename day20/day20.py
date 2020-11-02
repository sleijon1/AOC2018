from itertools import permutations
import re

def explore_path(regex, index, path, paths, copy):
    """ recursively explores all paths """
    index += 1
    print(regex[index])
    print(regex[index] == "|")
    if regex[index] == "$":
        print("end of regex")
        paths.append(path)
        return paths
    if regex[index] == "|":
        print("branch")
        paths.append(path)
        path = copy
        print(copy)
        return explore_path(regex, index, path, paths, copy)
    if regex[index] == "(":
        print("group")
        copy = path
        return explore_path(regex, index, path, paths, copy)
    if regex[index] == ")":
        return explore_path(regex, index, path, paths, copy)
    if regex[index] not in ("(", "|", "$", ")"):
        path += regex[index]
        print(path)
        return explore_path(regex, index, path, paths, copy)

if __name__ == "__main__":
    f = open("test2.txt", "r")
    regex = f.read().strip()
    print(regex)
    p = re.compile(regex)
    paths = explore_path(regex, 0, "", [], [])
    print(paths)




    #m = p.match("ENWWWSSEN")
    #groups = regex[1:-1]
    #groups = groups.split("(")
    #groups = [r.split("|") for r in groups]
    #for r in groups:
    #    for i, c in enumerate(r):
    #        r[i] = c.strip(")")
    #print(groups)
