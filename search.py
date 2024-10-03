from day import Day
from user import User
from output import Output
from sort import Sort

import os


class Search:
    # search keywords
    dtm = 'dtm:'
    dtm_len = len(dtm)
    lvl = 'lvl:'
    lvl_len = len(lvl)
    ctxt = 'ctxt:'
    ctxt_len = len(ctxt)

    def __init__(self, sorter: Sort):
        self.sorter: Sort = sorter

        # default search params
        self.start_rel_index: int = self.sorter.first_rel_index
        self.end_rel_index: int = self.sorter.last_rel_index
        self.level: int = 1  # whole day scope for search (instead of individual ptr level)
        self.context: int = 1  # num of ptrs shown b4 and after hit

        # track non range search (e.g., 1/2/34, //2024, /8/, 1//23, etc)
        self.generic_date = []

        self.is_valid_search = False  # whether is valid
        self.error_code = -1  # track error in search
        self.keyword_error = ''  # track keyword that had error

        self.search_clauses = []  # store clauses to search

        self.finds_day_is: list[int] = []  # keep track of indicies of days with find
        self.finds_is: list[list[int]] = []  # keep track of indicies of ptrs with finds

    def parse_search(self, words: str):
        ind_search_words = words.split()
        num_search_words = len(ind_search_words)

        i = 0
        while i < num_search_words:
            search_clause = ''
            add_search_clause = True

            search_word = ind_search_words[i]

            # exact search
            if search_word[0] == '\"' and len(search_word) > 1:
                search_word = search_word[1:]
                while True:
                    search_clause += search_word + ' '

                    # if last word
                    if i == num_search_words - 1:
                        if search_word[-1] == '\"':
                            search_clause = search_clause[:-2]
                        break
                    elif search_word[-1] == '\"':
                        search_clause = search_clause[:-2]
                        break

                    i += 1
                    search_word = ind_search_words[i]

            # search keywords
            elif ':' in search_word:
                # date search
                if search_word[:self.dtm_len] == self.dtm:
                    # keep track of which keyword could cause an error
                    self.keyword_error = self.dtm

                    # get rid of keyword
                    dtm_search = search_word[self.dtm_len:]

                    # range search
                    if '-' in search_word:
                        dtm_range = dtm_search.split('-')
                        start_range = -1

                        # only change start range from -1 (syntax error) if two elements
                        if len(dtm_range) == 2:
                            start_range = Day.date_to_index(dtm_range[0], self.sorter.is_euro_date, True)

                        # not an error
                        if start_range >= 0:
                            self.start_rel_index = start_range
                        else:
                            self.is_valid_search = False
                            self.error_code = start_range
                            return

                        end_range = Day.date_to_index(dtm_range[0], self.sorter.is_euro_date, True)
                        if end_range >= 0:
                            self.end_rel_index = end_range
                        else:
                            self.is_valid_search = False
                            self.error_code = end_range
                            return

                    # not a range
                    else:
                        self.generic_date = Day.date_to_index(dtm_search, self.sorter.is_euro_date)
                        if not isinstance(self.generic_date, (list, tuple)):
                            # error parsing
                            if self.generic_date < 0:
                                self.is_valid_search = False
                                self.error_code = self.generic_date
                                return
                            # specific date not in range of users pointers
                            elif not self.sorter.first_rel_index < self.generic_date < self.sorter.last_rel_index:
                                self.is_valid_search = False
                                self.error_code = -3
                                return
                            # must be a valid specific date
                            else:
                                # make range just that day
                                self.start_rel_index = self.generic_date
                                self.end_rel_index = self.generic_date
                                # reset generic so we know not to check that
                                self.generic_date = []

                    #  start date must be <= end date, otherwise invalid
                    if self.start_rel_index > self.end_rel_index:
                        self.is_valid_search = False
                        self.error_code = -2
                        return

                # change level of search
                elif search_word[:self.lvl_len] == self.lvl:
                    # keep track of which keyword could cause an error
                    self.keyword_error = self.lvl

                    if search_word[self.lvl_len:] == '0':
                        # all words have to be in one ptr
                        level = 0
                    elif search_word[self.lvl_len:] != '1':
                        self.is_valid_search = False
                        self.error_code = -2
                        return

                # change number of lines
                elif search_word[:self.ctxt_len] == self.ctxt:
                    # keep track of which keyword could cause an error
                    self.keyword_error = self.ctxt

                    # cant be a negative number
                    if search_word[self.ctxt_len].isdigit():
                        self.context = int(search_word[self.ctxt_len:])
                    else:
                        self.is_valid_search = False
                        self.error_code = -2
                        return

                # don't add any keywords as search clauses
                add_search_clause = False

            # not a special search so just add
            else:
                search_clause = search_word

            if add_search_clause:
                self.search_clauses.append(search_clause)

            i += 1

        self.is_valid_search = True

    def do_search(self):
        is_last_clause_found: int = 0  # count number of consecutive finds (to remove previous finds if &&)
        is_last_clause_and: bool = False
        is_find = False  # track if there are finds on the given day
        for day_i in range(self.start_rel_index, self.end_rel_index + 1):
            for clause in self.search_clauses:
                # clause to left and right both must be finds
                if clause == '&&':
                    is_last_clause_and = True
                    continue
                # if last clause before and was not found, skip
                elif is_last_clause_and and not is_last_clause_found:
                    is_last_clause_and = False
                    continue

                day: Day = self.sorter.days[self.sorter.rel_index_to_user_days(day_i)]
                if self.generic_date:
                    if not day.is_match_generic_date(self.generic_date, self.sorter.is_euro_date):
                        break  # go to next day
                finds = [find_i for find_i, ptr in enumerate(day.ptrs) if clause in ptr]

                if finds:
                    # first find on day
                    if not is_find:
                        self.finds_day_is.append(day_i)
                        self.finds_is.append(finds)
                    # not first find (just add indicies, not day)
                    else:
                        self.finds_is[-1] = list(set(self.finds_is[-1] + finds))

                    is_last_clause_found += 1
                    is_find = True
                else:
                    # remove previous finds because one wasn't found
                    if is_last_clause_and:
                        for i in range(is_last_clause_found):
                            self.finds_day_is.pop()
                            self.finds_is.pop()

                    # reset back to 0 because last not found
                    is_last_clause_found = 0

                # last clause no longer and
                is_last_clause_and = False

            # only sort once for efficiency
            if is_find:
                self.finds_is[-1] = sorted(self.finds_is[-1])
                is_find = False

    def print_search_finds(self):
        for day_i in self.finds_day_is:
            print('yo')

    def get_search_error_output(self):
        if self.error_code == -1:
            return Output.syntax_error_o
        elif self.error_code == -2:
            return Output.keyword_error_o
        elif self.error_code == -3:
            return Output.date_range_error_o
