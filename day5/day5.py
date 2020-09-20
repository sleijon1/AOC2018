import sys
sys.path.append("../")
sys.setrecursionlimit(1500)

from day1.day1part2 import read_and_strip

def wooga(string):
    """ Recursively removes every occurence of an upper case following a lower case
    or vice versa of the same character in string. """

    unique_characters = set(string.lower())
    processed_string = string
    for character in unique_characters:
        processed_string = processed_string.replace(character + character.upper(), "")
        processed_string = processed_string.replace(character.upper() + character, "")

    if len(processed_string) == len(string):
        return string

    return wooga(processed_string)

def booga(original_string):
    """ Iteratively removes all occurences of a character to optimize result
    of wooga. """
    unique_characters = set(original_string.lower())
    best_result = None
    stripped_string = None

    for char in unique_characters:
        stripped_string = original_string.replace(char, "").replace(char.upper(), "")
        result = wooga(stripped_string)
        if (best_result is None) or len(result) < len(best_result):
            best_result = result
            new_string = stripped_string

    optimized = wooga(new_string)

    return optimized

if __name__ == "__main__":
    input_string = read_and_strip()[0]
    result = wooga(input_string)
    optimized_result = booga(input_string)
    print(len(optimized_result))
