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
        self.start_rel_index = 0
        self.end_rel_index = self.sorter.num_days
        self.level = 1  # whole day scope for search (instead of individual ptr level)
        self.context = 1  # num of ptrs shown b4 and after hit

        # track non range search (e.g., 1/2/34, //2024, /8/, 1//23, etc)
        self.singular_date = []

        self.is_valid_search = False  # whether is valid
        self.error_code = -1  # track error in search
        self.keyword_error = ''

        self.search_clauses = []  # store clauses to search

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
                            start_range = Day.date_to_index(dtm_range[0], True)

                        # not an error
                        if start_range >= 0:
                            self.start_rel_index = start_range
                        else:
                            self.is_valid_search = False
                            self.error_code = start_range
                            return

                        end_range = Day.date_to_index(dtm_range[0], True)
                        if end_range >= 0:
                            self.end_rel_index = end_range
                        else:
                            self.is_valid_search = False
                            self.error_code = end_range
                            return

                    # not a range
                    else:
                        self.singular_date = Day.date_to_index(dtm_search)
                        if not isinstance(self.singular_date, (list, tuple)):
                            if self.singular_date < 0:
                                self.is_valid_search = False
                                self.error_code = self.singular_date
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
                self.search_clauses = search_clause

            i += 1

        self.is_valid_search = True

    def get_search_error_output(self):
        ret = ""
        if self.error_code == -1:
            ret = Output.syntax_error_o
        elif self.error_code == -2:
            ret = Output.keyword_error_o
        elif self.error_code == -3:
            ret = Output.date_range_error_o

        return ret + f' (keyword = {self.keyword_error}'

    def reset_searcher(self):
        self.start_rel_index = 0
        self.end_rel_index = self.sorter.num_days
        self.level = 1  # whole day scope for search (instead of individual ptr level)
        self.context = 1  # num of ptrs shown b4 and after hit

        # track non range search (e.g., 1/2/34, //2024, /8/, 1//23, etc)
        self.singular_date = []

        self.is_valid_search = False  # whether is valid
        self.error_code = -1  # track error in search

        self.search_clauses = []  # store clauses to search
