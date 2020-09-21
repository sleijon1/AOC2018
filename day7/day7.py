import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

class Node:
    def __init__(self, name):
        self.name = name
        self.dependencies = []

    def add_dependency(self, node):
        self.dependencies.append(node)

    def __str__(self):
        return ("Node (" + str(self.name) + ", " + str(self.dependencies) + ")")

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name)
    

def format_input(inp):
    formatted_list = []
    for entry in inp:
        split_entry = entry.split(" ")
        node = Node(split_entry[1])
        dependency = Node(split_entry[7])
        
        # if equal node already in list use that node
        if node in formatted_list:
            node = formatted_list[formatted_list.index(node)]
        else:
            formatted_list.append(node)
        node.add_dependency(dependency)
        
    return formatted_list
if __name__ == "__main__":
    inp = read_and_strip()
    
    n1 = Node('C')
    n2 = Node('A')
    
    n1.add_dependency(n2)
    #print(n1)
    n2.add_dependency(Node('B'))
    #print(n1)
    #n1.add_dependency(Node('F'))
    #print(inp)
    
    print(format_input(inp))
