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

    def __init__(self, ptrs_path):
        self.days: list[Day] = []
        self.has_ptrs = False
        with open(ptrs_path, 'r') as file:
            for line in file:
                day: Day = Day(line.strip())
                self.days.append(day)

                # are there any pointers written
                if day.has_ptrs():
                    self.has_ptrs = True

        self.num_days = len(self.days)

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

    # go to previous day or wrap around
    def prev_day(self, day):
        return (day - 1 + self.num_days) % self.num_days

    def determine_search(self, words):
        ind_words = words.split()
        searches: list[str | Any] = []
        num_words = len(ind_words)

        # default search params
        # search all days
        start = 0
        end = self.num_days
        # ind date search
        only = []
        level = 1  # search whole day for words
        context = 1  # num of ptrs b4 and after hit

        # search keywords
        dtm = 'dtm:'
        dtm_len = len(dtm)
        lvl = 'lvl:'
        lvl_len = len(lvl)
        ctxt = 'ctxt:'
        ctxt_len = len(ctxt)

        i = 0
        while i < num_words:
            # if search keyword, we don't add clause
            clause = ''
            add_clause = True

            word = ind_words[i]

            # exact search
            if word[0] == '\"' and len(word) > 1:
                word = word[1:]
                # make whole search enclosed in "" one clause
                while True:
                    clause += word + ' '

                    # if last word
                    if i == num_words - 1:
                        break
                    # remove trailing "
                    elif word[-1] == '\"':
                        clause = clause[:-2]
                        break

                    i += 1
                    word = ind_words[i]

            # search keywords
            elif ':' in word:
                if word[:dtm_len] == dtm:
                    dtm_search = word[dtm_len:]

                    # range search
                    if '-' in word:
                        dtm_range = dtm_search.split('-')
                        start_range = -1
                        # only change start range from -1 (syntax error) if two elements
                        if len(dtm_range) == 2:
                            start_range = self.convert_date_to_index(dtm_range[0], True, True)[0]

                        if start_range >= 0:
                            start = start_range
                        else:
                            return check_date_validity_return(start_range, dtm)

                        end_range = self.convert_date_to_index(dtm_range[1], True)[0]
                        if end_range >= 0:
                            end = end_range
                        else:
                            return check_date_validity_return(start_range, dtm)

                        add_clause = False

                    # not a range
                    else:
                        only = self.convert_date_to_index(dtm_search)

                # change level of search
                elif word[:lvl_len] == lvl:
                    if word[lvl_len:] == '0':
                        # all words have to be in one ptr
                        level = 0
                    elif word[lvl_len:] != '1':
                        return ['', f'\"{lvl}\"']

                    add_clause = False

                elif word[:ctxt_len] == ctxt:
                    if word[ctxt_len].isdigit():
                        context = int(word[ctxt_len:])
                    else:
                        return ['', f'\"{ctxt}\"']

                    add_clause = False

            # not a special search
            else:
                clause = word

            if add_clause:
                searches.append(clause)
            i += 1

        return [start, end, only, level, context] + searches

    def get_index_of_day(self, day, month, year):
        return Day.get_index(self.days[0], self.days[self.num_days - 1], day, month, year)

    def convert_date_to_index(self, date, is_range=False, is_start=False):
        if not date:  # empty
            if not is_range:
                # can't give an empty date if not a range, so return -1 = error
                return [-3]
            if not is_start:
                # if it is range and its the end of range, return -1 = last day
                return [self.num_days - 1]
            # must be start of range, so return 0
            return [0]

        # get date number
        day = ''
        for letter in date:
            if letter.isdigit():
                day += letter
            else:
                break

        # get year
        year = ''
        for letter in reversed(date):
            if letter.isdigit():
                year += letter
            else:
                break
        year = year[::-1]  # flip back around as added in reverse

        mth = date[len(day):-len(year)]
        month = Day.is_three_letter_month(mth)
        if month == -1:
            return [-3]

        # if we have a range, we must give a specific date (can't just be
        # sum like 13nov or nov2024 (can be for individual date search tho))
        if is_range:
            if not year or not day:
                return [-3]
            else:
                return [day, month, year]

        return [self.get_index_of_day(day, month, year)]
