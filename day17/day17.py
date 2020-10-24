import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

def format_input(inp):
    """ formats input as [(static axis, val), (ranging axis, start, end)] """
    formatted = []
    for entry in inp:
        new_entry = []
        static, clay = entry.split(",")
        clay = clay.strip().split("..")
        x_y, start = clay[0].split("=")
        end = int(clay[1])
        static = static.split("=")
        static[1] = int(static[1])
        new_entry.append(tuple(static))
        new_entry.append((x_y, int(start), end))
        formatted.append(new_entry)
    #print(formatted)
    return formatted

def print_map(map_):
    for row in map_:
        string = ""
        for col in row:
            string = col + string
        print(string)

def create_map(inp):
    """ creates map from formatted input """
    all_x = []
    all_y = []
    for entry in inp:
        if entry[0][0] == 'x':
            all_x.append(entry[0][1])
            all_y.append(entry[1][2])
            all_y.append(entry[1][1])
        elif entry[0][0] == 'y':
            all_y.append(entry[0][1])
            all_x.append(entry[1][2])
            all_x.append(entry[1][1])

    map_ = []
    # water can flow on the side of the min and max x's
    min_x = min(all_x)-1
    max_x = max(all_x)+1
    min_y = 0
    for y in range(min_y, max(all_y)+1):
        row = []
        for x in range(min_x-1, max_x):
            row.append(".")
        map_.append(row)

    for clay in inp:
        if clay[0][0] == 'x':
            for y in range(clay[1][1], clay[1][2]+1):
                map_[y][max_x-clay[0][1]] = "#"
        elif clay[0][0] == 'y':
            for x in range(clay[1][1], clay[1][2]+1):
                map_[clay[0][1]][max_x-x] = "#"
    # water spring
    map_[0][max_x-500] = "+"
    print_map(map_)
    return map_

def tick(map_):
    """ flows water one unit forward """
    
    pass

if __name__=="__main__":
    inp = read_and_strip(file_name="test.txt")
    f_inp = format_input(inp)
    for n in f_inp:
        print(n)
    map_ = create_map(f_inp)

