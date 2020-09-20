"""this module solves day4"""
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

import datetime

class Guard:
    """ A class representing a guard"""
    def __init__(self, id_num):
        """ constructor Guard
        Keyword args:
        id_num = the id of the guard
        """
        self.id_num = id_num
        self.sleep_schedule = {}

    def total_sleep(self):
        """ Returns total minutes slept """
        return sum(self.sleep_schedule.values())

    def minute_most_sleep(self):
        """ Returns the minute that the guard sleeps on the most or none if
        they havent slept. """

        try:
            max_slept = max(self.sleep_schedule.values())
        except ValueError:
            print("ValueError; Guard: " + str(self.id_num) + ", hasnt slept.")
            return None, None

        for key in self.sleep_schedule.keys():
            if self.sleep_schedule[key] == max_slept:
                return key, max_slept

    def add_minute(self, minute):
        """ adds a time slept at minute minute"""
        try:
            # increment time slept at this minute
            self.sleep_schedule[minute] += 1
        except KeyError:
            # first time slept at this minute
            self.sleep_schedule[minute] = 1

    def __str__(self):
        return 'Guard: ' + str(self.id_num)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.id_num == other.id_num
        )

def calculate_guard_sleep(guard_schedule):
    """ generates guards and adds their number of sleep to their
    sleep schedule

    Keyword args:
    guard_schedule - the ordered list of guard shifts
    Returns:
    list of guards
    """
    guard_list = []
    current_guard = None

    fell_asleep = None
    for entry in guard_schedule:
        event = entry[1]
        time_stamp = entry[0]

        if ("Guard" in event):
            guard_id = event.split("#")[1].split(" ")[0] #extracts the id
            NEW_GUARD = Guard(guard_id)
            if (NEW_GUARD in guard_list):
                # get guard from guard_list
                guard_index = guard_list.index(NEW_GUARD)
                current_guard = guard_list[guard_index]
            else:
                # new guard, add
                guard_list.append(NEW_GUARD)
                current_guard = NEW_GUARD
        else: # no new guard, add minutes of sleep
            if ("falls asleep" in event):
                fell_asleep = datetime.datetime.fromisoformat(time_stamp)
            elif ("wakes up" in event):
                woke_up = datetime.datetime.fromisoformat(time_stamp)
                asleep = fell_asleep
                while (asleep != woke_up):
                    # get the minute guard was asleep
                    current_minute = asleep.timetuple()[4]
                    current_guard.add_minute(current_minute)
                    # 1 minute accounted for
                    asleep = asleep + datetime.timedelta(minutes=1)

    return guard_list

def sleepiest_guard(guard_list):
    """ calculates which guard slept the most
    Keyword args:
    guard_list - list of guards to compare
    """
    sleepiest_guard = guard_list[0]
    for guard in guard_list:
        if guard.total_sleep() > sleepiest_guard.total_sleep():
            sleepiest_guard = guard
    return sleepiest_guard

def consistent_guard(guard_list):
    """ returns the guard that is most consistenly asleep at
    a specific minute.

    Keyword args:
    guard_list - list of guards
    """
    sleepiest_guard = guard_list[0]
    for guard in guard_list:
        minute, max_slept = guard.minute_most_sleep()
        _, current_max = sleepiest_guard.minute_most_sleep()
        if(max_slept is None or current_max is None):
            continue
        if max_slept > current_max:
            sleepiest_guard = guard

    return sleepiest_guard


def format_and_order_schedule():
    """formats and order schedule by date by reading input.txt file
    """
    inp = read_and_strip()
    format_input = list()
    for entry in inp:
        date = entry.split(']')
        slice_object = slice(1, len(date[0]), 1)
        date[0] = date[0][slice_object] # removes first bracket
        format_input.append(date)
    format_input = sorted(format_input, key=lambda entry: entry[0])
    return format_input

if __name__ == "__main__":
    format_input = format_and_order_schedule()
    guard_list = calculate_guard_sleep(format_input)

    sleepiest_guard = sleepiest_guard(guard_list)
    minute, _ = sleepiest_guard.minute_most_sleep()
    print("Part 1: " + str(sleepiest_guard) + "\n(" + str(minute) \
          + " * " + str(sleepiest_guard.id_num) + ") = " + \
          str(minute * int(sleepiest_guard.id_num)) + "\n")

    consistent_guard = consistent_guard(guard_list)
    minute, _ = consistent_guard.minute_most_sleep()
    print("\nPart 2: " + str(consistent_guard) + "\n(" + str(minute) \
          + " * " + str(consistent_guard.id_num) + ") = " + \
          str(minute * int(consistent_guard.id_num)))
