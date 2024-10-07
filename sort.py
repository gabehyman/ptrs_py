from typing import List, Any

from day import Day

import random as rand
import datetime


def check_date_validity_return(ret, dtm):
    if ret == -1:
        return ['-1', f'\"{dtm}\"']
    elif ret == -2:
        return ['-2']

    return ['-3']


class Sort:

    def __init__(self, ptrs_path, is_euro_date: bool):
        self.days: list[Day] = []
        self.has_ptrs = False
        self.is_euro_date: bool = is_euro_date

        # does nothing if no file
        with open(ptrs_path, 'r') as file:
            for line in file:
                day: Day = Day(line.strip(), self.is_euro_date)
                self.days.append(day)

                # are there any pointers written
                if day.has_ptrs():
                    self.has_ptrs = True

        self.num_days = len(self.days)
        self.first_rel_index = self.days[0].rel_index
        self.last_rel_index = self.days[self.num_days-1].rel_index

    def get_last_day(self):
        if not self.has_ptrs:
            return len(self.days) - 1  # show last day if no ptrs written
        else:
            # get last day with ptrs
            for i in reversed(range(len(self.days))):
                if self.days[i].has_ptrs():
                    return i

    def get_rand_day(self):
        # no ptrs have been written
        if self.has_ptrs:
            # don't show days with no ptrs written
            while True:
                day = rand.randrange(len(self.days))  # rando day
                if self.days[day].has_ptrs():
                    return day
                else:
                    continue
        else:
            return -1

    # go to next day or wrap around
    def next_day(self, day):
        return (day + 1) % self.num_days

    def rel_index_to_user_days(self, rel_index: int):
        return rel_index - self.first_rel_index

    # go to previous day or wrap around
    def prev_day(self, day):
        return (day - 1 + self.num_days) % self.num_days
