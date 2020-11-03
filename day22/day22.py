from collections import deque
from copy import deepcopy
from time import sleep

depth = 11109
target_x, target_y = (9, 731)
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
    for x in range(target_x+15):
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
    for key in erosion_levels:
        mod = erosion_levels[key] % 3
        if mod == 2:
            type_dict[key] = '|'
        elif mod == 1:
            type_dict[key] = '='
        elif mod == 0:
            type_dict[key] = '.'
    queue = deque()
    queue.append([[], 0, "torch", (0, 0)])
    visited = list()
    time = []
    cost_table = {(0, 0):
                  (0, "torch")}
    while True:
        if not queue:
            break
        current = queue.pop()
        visited.append(current)
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        path, minutes, tool, pos = current
        new_path = list(path)

        new_path.append(pos)
        if pos == (target_x, target_y):
            print("Solution part 2:\nFound Santa's friend in: " + str(minutes) + " minutes.")
            exit()
        x, y = pos
        queue_items = [(x+direction[0], y+direction[1]) for
                       direction in directions
                       if (x+direction[0], y+direction[1]) in type_dict.keys()]
        new_nodes = []
        for item in queue_items:
            if type_dict[item] == '.' and item == (target_x, target_y):
                if tool != "torch":
                    new_nodes.append([new_path, minutes+8, "torch",
                                      item])
                else:
                    new_nodes.append([new_path, minutes+1, tool, item])
            elif type_dict[item] == '.':
                if tool not in ("torch", "climbing_gear"):
                    new_nodes.append([new_path, minutes+8, "torch",
                                       item])
                    new_nodes.append([new_path, minutes+8,
                                      "climbing_gear",
                                      item])
                else:
                    new_nodes.append([new_path, minutes+1, tool, item])
            elif type_dict[item] == '|':
                if tool not in ("torch", "neither"):
                    new_nodes.append([new_path, minutes+8, "torch",
                                       item])
                    new_nodes.append([new_path, minutes+8, "neither",
                                       item])
                else:
                    new_nodes.append([new_path, minutes+1, tool, item])
            elif type_dict[item] == '=':
                if tool not in ("climbing_gear", " neither"):
                    new_nodes.append([new_path, minutes+8, "neither",
                                       item])
                    new_nodes.append([new_path, minutes+8,
                                      "climbing_gear",
                                       item])
                else:
                    new_nodes.append([new_path, minutes+1, tool, item])

        for new_node in new_nodes:
            try:
                # (cost, tool)
                key = (new_node[-1], new_node[2])
                if cost_table[key] <= new_node[1]:
                    continue
            except KeyError:
                cost_table[key] = new_node[1]

            queue.appendleft(new_node)
            visited.append(new_node)
        new_deck = list(queue)
        new_deck = sorted(new_deck, key=lambda x: x[1])
        list.reverse(new_deck)
        queue = deque(new_deck)
    print(time)
part_one()
part_two()
