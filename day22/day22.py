from time import sleep
from collections import deque
from copy import deepcopy

depth = 510
target_x, target_y = (10,10)
geologic_index = {
    (0, 0): 0,
    (target_x, target_y): 0,
}
erosion_levels = {
    (0, 0): depth%20183,
    (target_x, target_y): depth%20183,
}

def part_one():
    for x in range(target_x+1):
        for y in range(target_y+1):
            if (x == 0 and y == 0) or (x == target_x and y == target_y):
                continue
            elif y == 0:
                geologic_index[(x, y)] = x*16807
            elif x == 0:
                geologic_index[(x, y)] = y*48271
            else:
                geologic_index[(x, y)] = erosion_levels[(x-1, y)] \
                    * erosion_levels[(x, y-1)]
            erosion_levels[(x, y)] = (geologic_index[(x, y)] + depth) % 20183

    print("Solution part 1: " + str(sum([erosion % 3 for erosion in erosion_levels.values()])))

def part_two():
    for x in range(target_x+1):
        for y in range(target_y+1):
            if (x == 0 and y == 0) or (x == target_x and y == target_y):
                continue
            elif y == 0:
                geologic_index[(x, y)] = x*16807
            elif x == 0:
                geologic_index[(x, y)] = y*48271
            else:
                geologic_index[(x, y)] = erosion_levels[(x-1, y)] \
                    * erosion_levels[(x, y-1)]
            erosion_levels[(x, y)] = (geologic_index[(x, y)] + depth) % 20183
    type_dict = {}
    for key in erosion_levels.keys():
        mod = erosion_levels[key] % 3
        if mod == 2:
            type_dict[key] = '|'
        elif mod == 1:
            type_dict[key] = '='
        elif mod == 0:
            type_dict[key] = '.'
    queue = deque()
    queue.append([[], 0, "torch", 0, (0, 0)])
    visited = list()
    time = []
    while True:
        if not queue:
            break
        current = queue.pop()
        visited.append(current)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        path, minutes, tool, swaps, pos = current
        new_path = list(path)
        new_path.append(pos)
        #print("queue: " + str(queue))
        #sleep(1)
        if pos == (target_x, target_y):
            #if tool != "torch":
                #minutes += 7
            print("Found mans in: " + str(minutes) + " minutes.")
            print("Path: " + str(path))
            print("Current: " + str(current))
            exit()
        print("current node: " + str(current))
        #print(visited)
        x, y = pos
        #if (x, y) == (10, 9):
        #    exit()
        queue_items = [(x+direction[0], y+direction[1]) for
                       direction in directions
                       if (x+direction[0], y+direction[1]) in type_dict.keys()
                       and (x+direction[0], y+direction[1]) not in new_path]
        #print("queue_items: " + str(queue_items))
        new_nodes = []
        for item in queue_items:
            #print("current item: " + str(item))
            #print("type dict item: " + str(type_dict[item]))
            if type_dict[item] == '.':
                if tool not in ("torch", "climbing_gear"):
                    new_nodes.append([new_path, minutes+8, "torch",
                                      swaps+1, item])
                    new_nodes.append([new_path, minutes+8,
                                      "climbing_gear",
                                      swaps+1, item])
                else:
                    new_nodes.append([new_path, minutes+1, tool, swaps, item])
            elif type_dict[item] == '|':
                if tool not in ("torch", "neither"):
                    new_nodes.append([new_path, minutes+8, "torch",
                                      swaps+1, item])
                    new_nodes.append([new_path, minutes+8, "neither",
                                      swaps+1, item])
                else:
                    new_nodes.append([new_path, minutes+1, tool, swaps, item])
            elif type_dict[item] == '=':
                if tool not in ("climbing_gear", " neither"):
                    new_nodes.append([new_path, minutes+8, "neither",
                                      swaps+1, item])
                    new_nodes.append([new_path, minutes+8,
                                      "climbing_gear",
                                      swaps+1, item])
                else:
                    new_nodes.append([new_path, minutes+1, tool, swaps, item])
        #print("new_nodes: " + str(new_nodes))
        #print("len new nodes: " + str(len(new_nodes)))
        #new_nodes = sorted(new_nodes, key=lambda x: x[1])
        #new_nodes.reverse()
        for new_node in new_nodes:
            same_nodes = [visit for visit in visited
                         if visit[-1] == new_node[-1]
                         and visit[1] <= new_node[1]]
            if same_nodes:
               continue
            queue.appendleft(new_node)
            visited.append(new_node)
        #print(queue)
        new_deck = list(queue)
        new_deck = sorted(new_deck, key=lambda x: x[1])
        list.reverse(new_deck)
        queue = deque(new_deck)
        #print(new_deck)


part_one()
part_two()
