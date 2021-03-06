import unittest
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

ASCII_VALUE_OFFSET = 64

class WorkerTestCase(unittest.TestCase):
    """ Testing basic Worker class functionality """
    def setUp(self):
        self.worker = Worker("worker 1")
        self.worker.assign("D")

    def test_tick(self):
        self.worker.tick(0)
        self.worker.tick(0)
        self.worker.tick(0)
        self.assertEqual(self.worker.work, 'D', "tick not working 2")
        self.worker.tick(0)
        self.assertEqual(self.worker.record, ['D', 'D', 'D', 'D'], "tick not working")
        self.assertEqual(self.worker.work, '.', "tick not working 2")


class Worker:
    def __init__(self, name):
        """
        name - name of worker
        work - node currently working on (. if no current work)
        record - record of what worker is doing each second
        """
        self.name = name
        self.work = "."
        self.record = []

    def assign(self, work):
        self.work = work

    def tick(self, time_constant=0):
        """ advances the time by a problem second """
        self.record.append(self.work)
        if self.work != '.':
            if self.record.count(self.work) == ord(self.work) + time_constant - ASCII_VALUE_OFFSET:
                work_done = self.work
                self.work = '.'
                return work_done
            else:
                return None
        return None

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    def last_worked(self):
        """ calculates the latest second that the Worker instance
        had work in their record"""
        time = 0
        for i in range(0, len(self.record)):
            if self.record[i] != '.':
                time = i
        return time

def create_workers(workers=2):
    """ Creates workers amount of workers and returns them in a list """
    worker_list = []
    for i in range(1, workers+1):
        new_worker = Worker("Worker " + str(i))
        worker_list.append(new_worker)
    return worker_list


def calculate_traversal_timed(node_list, wrkers=5, time_constant=0):
    """ Calculate traversal respecting dependency and time it takes for each
    node
    Keyword arguments:
    node_list -- list of dependencies
    wrkers -- amount of workers that can be assigned work
    """
    workers = create_workers(wrkers)
    print(workers)
    unique_entries = []
    for node in node_list:
        if node[0] not in unique_entries:
            unique_entries.append(node[0])
        if node[1] not in unique_entries:
            unique_entries.append(node[1])

    traversal = []
    end_nodes = []
    while len(traversal) != len(unique_entries):
        possible_nodes = calculate_next_step(node_list)
        current_work = []
        for worker in workers:
            current_work.append(worker.work)
        print("current work: " + str(current_work))

        # remove possible nodes that are worked on currently
        possible_nodes = [pnode for pnode in possible_nodes if pnode[0] not in current_work]
        if all(work=='.' for work in current_work) and possible_nodes == []:
            # we have end nodes left
            for entry in unique_entries:
                if entry not in traversal:
                    pnode_names.append(entry)
            print("end nodes: " + str(pnode_names))
        else:
            pnode_names = list(set([dep[0] for dep in possible_nodes]))
        pnode_names.sort()
        print("pnode_names: " + str(pnode_names))

        # assign work
        for i in range(0, len(pnode_names)):
            for worker in workers:
                if worker.work == '.':
                    worker.assign(pnode_names[i])
                    break

        # advance every worker one second
        for worker in workers:
            tick_result = worker.tick(time_constant)
            if tick_result is not None:
                traversal.append(tick_result)

        # remove traversed nodes
        node_list = [node for node in node_list if node[0] not in traversal]

    return traversal, workers


def calculate_traversal(node_list):
    """ Calculate traversal respecting dependency """
    workers = create_workers()
    print(workers)
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
        pnode_names = list(set([dep[0] for dep in possible_nodes]))
        print("pnode_names: " + str(pnode_names))
        # sort alphabetically between all possible node steps
        possible_nodes.sort(key = lambda node: node[0])
        print("possible nodes: " + str(possible_nodes))

        traversed_node = possible_nodes[0][0]
        traversal.append(traversed_node)
        # remove traversed node
        node_list = [node for node in node_list if node[0] != traversed_node]
    return traversal

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

def suite():
    """ Simple test suite """
    suite = unittest.TestSuite()
    suite.addTest(WorkerTestCase('test_tick'))
    return suite

def last_worked_workers(workers):
    """ calls last_worked() on workers and returns list of the their
    results
    """
    last_worked = []
    for worker in workers:
        print("\n " + str(worker) + "\n Last time worked: " + str(worker.last_worked()))
        last_worked.append(worker.last_worked())
    return last_worked

def test_simple():
    """ only works without time constant """
    inp_test = read_and_strip(file_name="input2.txt")
    node_test = format_input(inp_test)
    _, workers_test = calculate_traversal_timed(node_test, 2)
    last_worked = last_worked_workers(workers_test)
    bottleneck = max(last_worked)+1
    print(bottleneck)
    assert(bottleneck==15)
    return True

if __name__ == "__main__":
    test_simple()

    inp = read_and_strip(file_name="input.txt")
    node_list = format_input(inp)
    traversal_list, workers =  calculate_traversal_timed(node_list, 5, time_constant=60)
    print("".join(traversal_list))
    bottleneck = max(last_worked_workers(workers)) + 1 # add one since second starts at 0
    print("Bottleneck: " + str(bottleneck))

    runner = unittest.TextTestRunner()
    runner.run(suite())

