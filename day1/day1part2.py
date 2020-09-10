"""this module solves day 1"""

def read_and_strip(element_type=None, file_name="input.txt"):
    """reads text file, strips newline and empty strings

    Keyword arguments:
    element_type -- the type to convert element to if any
    file_name -- the name of the file to read input from
    """
    text_file = open(file_name, "r")
    text_file_list = text_file.readlines()
    tf_list_strip = []

    for line in text_file_list:
        if line.strip() == "":
            continue
        elif element_type is None:
            tf_list_strip.append(line.strip())
        else:
            tf_list_strip.append(element_type(line.strip()))

    return tf_list_strip

def find_reoccuring_frequency(frequency_list):
    """finds when the current sum of frequency_list reaches the same number
    twice

    Keyword arguments:
    frequency_list - list of real numbers
    """
    unique_frequencies = []
    current_frequency = 0
    i = 0
    while True:
        for frequency in frequency_list:
            if current_frequency in unique_frequencies:
                return current_frequency
            unique_frequencies.append(current_frequency)
            current_frequency += frequency
        i += 1
        print("Repeating frequency list: " + str(i))


def run_day_one():
    """runs day one """
    frequencies = read_and_strip(int)
    sum_frequencies = sum(frequencies)
    print(sum_frequencies)

def run_day_one_ptwo():
    """runs day one part two"""
    frequencies = read_and_strip(int)
    reoccuring_frequency = find_reoccuring_frequency(frequencies)
    print(reoccuring_frequency)

if __name__ == "__main__":
    #run_day_one()
    run_day_one_ptwo()
