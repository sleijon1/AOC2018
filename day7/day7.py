import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

ASCII_VALUE_OFFSET = 64

class Node:
    def __init__(self, name):
        self.name = name
        self.dependencies = []

    def add_dependency(self, node):
        self.dependencies.append(node)
        self.dependencies.sort(key = lambda node: node.name)

    def __str__(self):
        return ("Node (" + str(self.name) + ", " + str(self.dependencies) + ")")

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name)

def calculate_traversal(node_list):
    """ Calculate traversal respecting dependency """
    unique_entries = []
    for node in node_list:
        if node[0] not in unique_entries:
            unique_entries.append(node[0])
        if node[1] not in unique_entries:
            unique_entries.append(node[1])

    traversal = []
    while len(traversal) < len(unique_entries):
        if len(node_list) == 1:
            # last dependency, add and done
            node = node_list[0]
            traversal.append(node[0])
            traversal.append(node[1])
            break
        possible_nodes = calculate_next_step(node_list)
        # sort alphabetically between all possible node steps
        possible_nodes.sort(key = lambda node: node[0])
        print(possible_nodes)
        traversed_node = possible_nodes[0][0]
        traversal.append(traversed_node)
        # remove traversed node
        node_list = [node for node in node_list if node[0] != traversed_node]
    #lambda c: ord(c)-96
    return traversal

def calculate_traversal_timed(node_list):
    """ Calculate traversal respecting dependency """
    unique_entries = []
    for node in node_list:
        if node[0] not in unique_entries:
            unique_entries.append(node[0])
        if node[1] not in unique_entries:
            unique_entries.append(node[1])

    traversal = []
    total_time = 1
    while len(traversal) < len(unique_entries):
        time_saved = 0
        if len(node_list) == 1:
            # last dependency, add and done
            node = node_list[0]
            traversal.append(node[0])
            traversal.append(node[1])
            break

        possible_nodes = calculate_next_step(node_list)
        # sort alphabetically between all possible node steps

        possible_nodes.sort(key = lambda node: node[0])
        pnode_names = []
        # ignore dependancy
        for pnode in possible_nodes:
            if pnode[0] not in pnode_names:
                pnode_names.append(pnode[0])
                traversal.append(pnode[0])
        pnode_names.sort(reverse=True)
        print(possible_nodes)
        if pnode_names != []:
            expensive = pnode_names[0]
            time_saved = sum([ord(expensive) - ord(pnode) for pnode in pnode_names])
        else:
            for step in unique_entries:
                if (step not in traversal):
                    pnode_names.append(step)
                    print(pnode_names)
                    traversal.append(step)
        time_consumed = sum([60 + ord(pnode)-ASCII_VALUE_OFFSET for pnode in pnode_names])
        print("time consumed: " + str(time_consumed))
        print("time saved: " + str(time_saved))
        total_time += time_consumed-time_saved

        # remove traversed nodes
        node_list = [node for node in node_list if node[0] not in pnode_names]
        #print("node_list aftre removal: " + str(node_list))
    return traversal, total_time

def calculate_next_step(node_list):
    """ calculates the possible steps and returns them as [(node, dependant)]"""
    #print(node_list)
    free_nodes = []
    free = None
    for node in node_list:
        free = True
        node_name = node[0]
        for node_two in node_list:
            if node_name in node_two[1]:
                free = False
                break
        if free:
            free_nodes.append(node)

    return free_nodes

def format_input(inp):
    """ Formats the input to [(node, dependant_node)]"""
    formatted_list = []
    for entry in inp:
        split_entry = entry.split(" ")
        node = split_entry[1]
        dependency = split_entry[7]
        formatted_list.append((node, dependency))

    return formatted_list

if __name__ == "__main__":
    inp = read_and_strip()

    node_list = format_input(inp)
    traversal_list, time = calculate_traversal_timed(node_list)
    print("".join(traversal_list))
    print(time)
