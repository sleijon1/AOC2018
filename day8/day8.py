import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

class Node:
    """ Node class with list of metadata and list of child nodes (makes up a tree)
    Keyword args:
    no_entries -- amount of metadata
    child_nodes -- amount of child nodes
    """
    
    def __init__(self, no_entries, no_nodes):
        self.metadata_entries = [0]*no_entries
        self.child_nodes = [None]*no_nodes
        
    def __str__(self):
        return "(Node: Children: " + str(self.child_nodes) +\
            ". MD Entries: " + str(self.metadata_entries) + ")"

    def __repr__(self):
        return str(self)
    
    def insert_entry(self, new_entry):
        """ inserts entry at first free position """
        for entry in self.metadata_entries:
            if entry == 0:
                self.metadata_entries[self.metadata_entries.index(entry)] = new_entry
                break
            
    def insert_node(self, new_node):
        """ inserts node at first free position """
        for node in self.child_nodes:
            if node is None:
                self.child_nodes[self.child_nodes.index(node)] = new_node
                break

    def node_value(self):
        """ Calculates the value of the node
        Value of node is recursively defined as
        value of child nodes indexed by metadata entries.
        Value of node with zero child nodes is sum of metadata entries.
        """
        value = 0
        if self.child_nodes == []:
            return sum(self.metadata_entries)

        for child_number in self.metadata_entries:
            child_number = child_number-1
            if child_number < len(self.child_nodes):
                child_value = self.child_nodes[child_number].node_value()
                value += child_value
                
        return value

def generate_tree(inp, start_index=0, root=None, metadata_sum=0):
    """ recursively generates the tree formed by input argument
    Keyword args:
    inp -- tree information input
    start_index -- index to start from (changed on each recursion)
    root -- None first iteration then the first node i.e. root
    metadata_sum -- 0 on first iteration then sum of the meta data
    up until a specific node

    """
    index = start_index
    no_nodes = inp[index]
    no_entries = inp[index+1]
    node = Node(no_entries, no_nodes)
    if root is None:
        root = node
            
    index = index+2
    
    for _ in node.child_nodes:
        new_node, new_index, metadata_sum = generate_tree(inp, index, root, metadata_sum)
        index = new_index
        node.insert_node(new_node)
    if None not in node.child_nodes:
        for _ in node.metadata_entries:
            new_entry = inp[index]
            node.insert_entry(new_entry)
            metadata_sum  += new_entry
            index += 1
        return node, index, metadata_sum

def format_input(inp):
    split_entries = inp[0].split(" ") # remove white space in input
    integer_entries = [int(entry) for entry in split_entries]
    return integer_entries

def test_Node():
    node = Node(3, 3)
    node2 = Node(3, 3)
    node3 = Node(5, 3)
    node.insert_entry(9)
    node.insert_entry(11)
    node.insert_node(node2)
    node.insert_node(node3)
    assert(node.metadata_entries == [9, 11, 0])
    assert(node.child_nodes == [node2, node3, None])
    print("Passed simple Node test.")

def calculate_tree_sum():
    return None
    
if __name__ == "__main__":
    small_input = read_and_strip(file_name="smaller_input.txt")
    s_input = format_input(small_input)
    test_Node() # simple Node test
    small_tree, _, md_sum = generate_tree(s_input) # ignore recursive index return
    assert(small_tree.node_value()==66)
    assert(md_sum==138)
    print("small tree test successful")
    #print(small_tree)


    
    problem_input = read_and_strip(file_name="input.txt")
    p_input = format_input(problem_input)
    problem_tree, _, md_sum2 = generate_tree(p_input)
    assert(md_sum2==48155)
    print("-----------\nproblem tree test successful")
    print("problem tree md sum: " + str(md_sum2))
    value = problem_tree.node_value()
    print("problem tree root value: " + str(value))
