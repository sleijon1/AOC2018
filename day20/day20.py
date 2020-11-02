import re
from collections import deque


def calc_dist(paths):
    rooms = {
        (0, 0): 0
    }
    for path in paths:
        step = 0
        room = (0, 0)
        for direction in path:
            step += 1
            if direction == 'W':
                room = (room[0]-1, room[1])
            if direction == 'N':
                room = (room[0], room[1]+1)
            if direction == 'E':
                room = (room[0]+1, room[1])
            if direction == 'S':
                room = (room[0], room[1]-1)
            try:
                if rooms[room] > step:
                    rooms[room] = step
            except KeyError:
                rooms[room] = step
    return rooms


def find_branches(regex, start, end):
    queue_items = []
    bl = br = 0
    last_branch = start
    for i in range(start, end):
        if regex[i] == "(":
            bl += 1
        elif regex[i] == ")":
            br += 1
        if (regex[i] == "|" or i == end-1) and br-bl == 0:
            queue_items.append(regex[last_branch:i+1].strip('|'))
            last_branch = i
    #print("queue_items: " + str(queue_items))
    return queue_items

def explore_path(regex):
    """ explores entire map using queue
    (Works but very slow)
    """
    queue = deque()
    queue.appendleft(["", regex])
    valid_paths = []
    p = re.compile(regex)
    while True:
        if not queue:
            break
        path_and_trail = queue.pop()
        trail = path_and_trail[0]
        path = path_and_trail[1]
        br = bl = 0
        cont = False
        for i, direction in enumerate(path):
            if direction == "(":
                for j in range(i, len(path)):
                    if path[j] == "(":
                        bl += 1
                    elif path[j] == ")":
                        br += 1
                    if bl - br == 0:
                        path_items = find_branches(path, i+1, j)
                        for item in path_items:
                            if path[j-1] == "|":
                                queue.appendleft([trail, path[j+1:]])
                                queue.appendleft([trail+item, path[j+1:]])
                            else:
                                queue.appendleft([trail, item])
                        cont = True
                        break
                if cont:
                    break
            else:
                #print(trail)
                trail += direction
        if cont:
            continue
        else:
            if not p.match(trail):
                exit()
            valid_paths.append(trail)
    #print(valid_paths)
    return valid_paths

directions = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}

def pro_solution(regex):
    """ inspiration from reddit """
    print(regex)
    x = y = 0
    positions = []
    steps = {}
    prev_x, prev_y = position = x, y
    steps[position] = 0
    for c in regex:
        if c == '(':
            positions.append(position)
            continue
        elif c == '|':
            position = positions[-1]
        elif c == ')':
            position = positions.pop()
        else:
            position = (position[0]+directions[c][0], position[1]+directions[c][1])
            print(position)
            try:
                steps[position] = min(steps[position], steps[(prev_x, prev_y)]+1)
            except KeyError:
                steps[position] = steps[(prev_x, prev_y)] + 1

        prev_x, prev_y = position

    print(steps)
    print("Solution Part 1: " + str(max(steps.values())))
    print("Solution Part 2: " + str(len([value for value in steps.values() if value >= 1000])))

if __name__ == "__main__":
    f = open("input.txt", "r")
    regex = f.read().strip()
    #paths = explore_path(regex[1:len(regex)-1])
    #rooms = calc_dist(paths)
    #print("Solution Part 1: " + str(max(rooms.values())))
    pro_solution(regex[1:-1])
