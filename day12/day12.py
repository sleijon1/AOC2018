import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

def create_schema(inp):
    """ Creates dict matching pattern to result """
    schema = {}
    initial_state = inp[0].split(":")[1].strip(" ")
    instructions = inp
    instructions.pop(0)
    for instruction in instructions:
        split = instruction.split("=>")
        pattern = split[0].strip(" ")
        result = split[1].strip(" ")
        schema[pattern] = result

    return schema, initial_state

def evolve_sequence(schema, sequence, empty, evolutions=20):
    """ evolves a sequence given certain schema """

    # will affect final sequence and number of plants
    sequence = "."*empty + sequence
    sequence = sequence + "."*empty
    for s in range(evolutions):
        print_seq = sequence.strip(".")
        new_sequence = ""
        for i, _ in enumerate(sequence):
            if i == 1 or i == 0 or \
               i == len(sequence)-1 or i == len(sequence)-2:
                new_sequence += sequence[i]
                continue
            current_pattern = sequence[i-2:i+3]
            try:
                new_sequence += schema[current_pattern]
            except KeyError as e:
                new_sequence += sequence[i]
        if sequence.strip(".") == new_sequence.strip("."):
            # sequence is repeating - stop
            break
        sequence = new_sequence
    return sequence

def count_index(sequence, offset):
    """ counts the index of the plants offsetting the plants
    before the "zeroth" plant """
    count = 0
    for i, char in enumerate(sequence):
        if char == "#":
            count += i-offset
    return count

def part2(repeating_seq_ind, generations=50000000000, plants=88, last_gen=124):
    """ counts the index for the plants after 50bil generations.
    Keyword args:
    repeating_seq_ind -- the index of the first occurence of
    the repeating seq
    generations -- the amount of generations
    plants -- amount of plants that move each iteration
    last_gen -- the last generation that affected the repeating sequence
    """
    return repeating_seq_ind  + (plants*(generations-last_gen))

if __name__ == "__main__":
    test_inp = read_and_strip(file_name="count_test.txt")
    assert(count_index(test_inp[-1], 3) == 325)

    inp = read_and_strip(file_name="problem_input.txt")
    schema, initial_state = create_schema(inp)
    empty = 127 # need 127 empty pots to get to steady state value
    end_sequence = evolve_sequence(schema, initial_state, empty, evolutions=125) # after 125 evolutions the plants just propagate through the empty pots to the right
    count = count_index(end_sequence, empty)
    print("Repeating sequence:\n" + str(end_sequence) + "\nIndex sum: " + str(count))
    print("\nPart 1: " + str(count_index(evolve_sequence(schema, initial_state, empty=24, \
                                                         evolutions=20), 24)))
    print("\nPart 2: " + str(part2(count)))
