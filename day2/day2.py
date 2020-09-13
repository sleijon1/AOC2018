""" this module solves day 2"""
import re
import string
import sys
from difflib import get_close_matches

sys.path.append("../")

from day1.day1part2 import read_and_strip

def find_occurence_exact(search_space, count, text):
    """Finds if an element of the search space occurs
    exactly count times in text

    Keyword arguments:
    search_space -- elements to search for
    count -- the amount of occurences
    text -- the string to search in
    """
    search_space = str(search_space)
    for element in search_space:
        occurence_list = re.findall(element, text)
        if len(occurence_list) == count:
            return True
    return False

def count_exact_twos_threes():
    """Calculate the product of the count of two and
    three reoccuring letters in the strings read from input.txt
    """
    alphabet = string.ascii_lowercase
    box_ids = read_and_strip()
    twos = 0
    threes = 0
    for id in box_ids:
        if find_occurence_exact(alphabet, 2, id):
            twos += 1
        if find_occurence_exact(alphabet, 3, id):
            threes += 1
    print(twos*threes)
    return twos, threes

def find_similar_string(matches, string, list_strings):
    """Return a string that has matches amount of matches with string.
    Does not find exact matches.

    Keyword arguments:
    matches -- amount of matches to fulfill
    string -- string to match against
    list_strings -- search space
    """
    if(matches > len(string)):
        raise Exception("Sorry, string can't have more matches than characters.")

    best_matches = get_close_matches(string, list_strings)
    # remove exact matches
    while string in best_matches: best_matches.remove(string)

    if len(best_matches) == 0:
        return None

    compare_string = best_matches[0]
    if sum([1 for i, j in zip(compare_string, string) if i == j]) == matches:
        return best_matches[0]

    return None

def find_matching_box_id():
    box_ids = read_and_strip()
    for id in box_ids:
        # suppose to match exactly except for one char
        no_matches = len(id)-1
        match = find_similar_string(no_matches, id, box_ids)
        if match is not None:
            return id, match
    return None

if __name__ == "__main__":
    #count_exact_twos_threes()
    print(find_matching_box_id())
