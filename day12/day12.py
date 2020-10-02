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

def evolve_sequence(schema, sequence, evolutions=20):
    """ evolves a sequence given certain schema """
    sequence = list(sequence)
    for i, _ in enumerate(sequence):
        if i == 1 or i == 0 or \
           i == len(sequence)-1 or i == len(sequence)-2:
            continue
        current_pattern = sequence[i-2:i+3]
        current_pattern = ''.join(current_pattern)
        print(current_pattern)
        try:
            sequence[i]  = schema[current_pattern]
        except KeyError as e:
            print(str(e) + "No schema found")
    sequence = ''.join(sequence)
    print(sequence)

if __name__ == "__main__":
    inp = read_and_strip(file_name="test_input.txt")
    schema, initial_state = create_schema(inp)
    evolve_sequence(schema, initial_state)
