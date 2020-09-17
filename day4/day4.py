"""this module solves day4"""
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

class Guard:
    """ A class representing a guarde"""
    def __init__(self, id_num):
        self.id_num = id_num
        self.sleep_schedule = {}

    def total_sleep(self):
        """ Returns total minutes slept """
        return sum(self.sleep_schedule.values())

    def minute_most_sleep(self):
        """ Returns the minute that the guard sleeps on the most"""
        return max(self.sleep_schedule.values())
    
        
def format_and_order_schedule():
    """formats and order schedule by date
    """
    inp = read_and_strip()
    format_input = list()
    for entry in inp:
        date = entry.split(']')
        slice_object = slice(1, len(date[0]), 1)
        date[0] = date[0][slice_object] # removes first bracket
        format_input.append(date)
    format_input = sorted(format_input, key=lambda entry: entry[0])
    print(format_input)

if __name__ == "__main__":
    #run_day_four()
    GUARD = Guard(15)
    GUARD.sleep_schedule[11] = 1
    print(GUARD.sleep_schedule)
