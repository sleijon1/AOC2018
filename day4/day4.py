"""this module solves day4"""
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

import datetime

class Guard:
    """ A class representing a guard"""
    def __init__(self, id_num):
        self.id_num = id_num
        self.sleep_schedule = {}

    def total_sleep(self):
        """ Returns total minutes slept """
        return sum(self.sleep_schedule.values())

    def minute_most_sleep(self):
        """ Returns the minute that the guard sleeps on the most"""
        max_slept = max(self.sleep_schedule.values())
        for key in self.sleep_schedule.keys():
            if self.sleep_schedule[key] == max_slept:
                return key

    def add_minute(self, minute):
        """ adds a time slept at minute minute"""
        try:
            # increment time slept at this minute
            self.sleep_schedule[minute] += 1
        except KeyError:
            # first time slept at this minute
            self.sleep_schedule[minute] = 1

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.id_num == other.id_num
        )

def calculate_guard_sleep(guard_schedule):
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

def sleepy_guard(guard_list):
    sleepiest_guard = guard_list[0]
    for guard in guard_list:
        if guard.total_sleep() > sleepiest_guard.total_sleep():
            sleepiest_guard = guard

    result = sleepiest_guard.minute_most_sleep() * int(sleepiest_guard.id_num)
    print(result)
    return result

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
    return format_input

if __name__ == "__main__":
    format_input = format_and_order_schedule()
    guard_list = calculate_guard_sleep(format_input)
    sleepy_guard(guard_list)

