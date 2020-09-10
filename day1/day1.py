"""reads text file, strips newline and empty strings

Keyword arguments:
element_type -- the type to convert element to if any
file_name -- the name of the file to read input from
"""
def read_and_strip(element_type=None, file_name="input.txt"):
    text_file = open(file_name, "r")
    text_file_list= text_file.readlines()
    tf_list_strip = []
        
    for line in text_file_list:
        if line.strip() == "":
            continue
        elif element_type is None:
            tf_list_strip.append(line.strip())
        else:
            tf_list_strip.append(element_type(line.strip()))
        
    return tf_list_strip

def run_day_one():
    frequencies = read_and_strip(int)
    sum_frequencies = sum(frequencies)
    return sum_frequencies
    
if __name__ == "__main__":
    assert run_day_one() == 466
    print(run_day_one())
