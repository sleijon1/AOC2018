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
        print(count_index(sequence, empty))
        #print("Sequence"+ "(" + str(s) + ")" +"\": " + ''.join(sequence))
        new_sequence = ""
        for i, _ in enumerate(sequence):
            if i == 1 or i == 0 or \
               i == len(sequence)-1 or i == len(sequence)-2:
                new_sequence += sequence[i]
                continue
            else:
                current_pattern = sequence[i-2:i+3]
            try:
                new_sequence += schema[current_pattern]
            except KeyError as e:
                new_sequence += sequence[i]
        sequence = new_sequence
    return sequence

def count_index(sequence, offset):
    count = 0
    for i, char in enumerate(sequence):
        if char == "#":
            count += i-offset
    return count

if __name__ == "__main__":
    test_inp = read_and_strip(file_name="count_test.txt")
    assert(count_index(test_inp[-1], 3) == 325)

    inp = read_and_strip(file_name="problem_input.txt")
    schema, initial_state = create_schema(inp)
    empty = 24
    end_sequence = evolve_sequence(schema, initial_state, empty, evolutions=50000000)
    count = count_index(end_sequence, empty)
    print(count)
    print(end_sequence, count)

#682137
#682135
#722263

