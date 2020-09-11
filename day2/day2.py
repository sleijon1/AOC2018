""" this module solves day 2"""
import re
import string
import sys
sys.path.append("../")

from day1.day1part2 import read_and_strip

def find_occurence_exact(search_space, count, text):
    search_space = str(search_space)
    for element in search_space:
        occurence_list = re.findall(element, text)
        if len(occurence_list) == count:
            return True
    return False

def count_exact_twos_threes():
    alphabet = string.ascii_lowercase
    print(find_occurence_exact(alphabet, 9, "dwkoood"))
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

if __name__ == "__main__":
    count_exact_twos_threes()
