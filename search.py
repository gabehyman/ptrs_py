from day import Day
from output import Output
from sort import Sort


class Search:
    # search keywords
    dtm: str = 'dtm:'
    dtm_len: int = len(dtm)
    lvl: str = 'lvl:'
    lvl_len: int = len(lvl)
    ctxt: str = 'ctxt:'
    ctxt_len: int = len(ctxt)

    def __init__(self, sorter: Sort):
        self.sorter: Sort = sorter

        # default search params
        self.start_rel_index: int = self.sorter.first_rel_index
        self.end_rel_index: int = self.sorter.last_rel_index
        self.level: int = 0  # whole day scope for search (instead of individual ptr level)
        self.context: int = 1  # num of ptrs shown b4 and after hit

        # track non range search (e.g., 1/2/34, //2024, /8/, 1//23, etc)
        self.generic_date: list[int] = []

        self.is_valid_search: bool = False  # whether is valid
        self.error_code: int = -1  # track error in search
        self.keyword_error: str = ''  # track keyword that had error

        self.search_clauses: list[str] = []  # store clauses to search (no repeats but order matters)
        self.actual_search_clauses: list[str] = []  # store index of non-&& clauses
        self.only_hasher_search: bool = True  # only searching hashers

        self.finds_day_is: list[int] = []  # keep track of indicies of days with find (not a set cuz ordered)
        self.finds_actual_clauses: list[list[int]] = []  # keep track of indicies of clauses that were actually found
        self.finds_is: list[list[int]] = []  # keep track of indicies of ptrs with finds (not a set cuz ordered)
        self.num_days_find: int = 0
        self.num_finds: int = 0

    # parse search and set all fields of object based on search
    def parse_search(self, words: str):
        ind_search_words: list[str] = words.split()
        num_search_words: int = len(ind_search_words)
        last_clause_dup = False

        i: int = 0
        while i < num_search_words:
            search_clause: str = ''
            add_search_clause: bool = True

            search_word: str = ind_search_words[i]

            # exact search
            if search_word[0] == '\"':
                search_word = search_word[1:]  # truncate to remove "
                while True:  # iterate until next " or end of word
                    search_clause += search_word

                    # remove last " (also account for " then space)
                    if len(search_word) != 0 and search_word[-1] == '\"':
                        search_clause = search_clause[:-1]
                        break

                    # no space for last word
                    if i != num_search_words - 1:
                        search_clause += ' '
                    else:
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
                    if '-' in dtm_search:
                        dtm_range = dtm_search.split('-')
                        start_range: int = -1

                        # only change start range from -1 (syntax error) if two elements
                        if len(dtm_range) == 2:
                            start_range = Day.date_to_index(dtm_range[0], self.sorter.is_euro_date, True)[0]

                        # not an error
                        if start_range >= 0:
                            self.start_rel_index = start_range
                        else:
                            self.is_valid_search = False
                            self.error_code = start_range
                            return

                        end_range: int = Day.date_to_index(dtm_range[1], self.sorter.is_euro_date, True)[0]
                        if end_range >= 0:
                            self.end_rel_index = end_range
                        else:
                            self.is_valid_search = False
                            self.error_code = end_range
                            return

                    # not a range
                    else:
                        self.generic_date = Day.date_to_index(dtm_search, self.sorter.is_euro_date)
                        if len(self.generic_date) != 3:
                            # error parsing
                            if self.generic_date[0] < 0:
                                self.is_valid_search = False
                                self.error_code = self.generic_date[0]
                                return
                            # specific date not in range of users pointers
                            elif not self.sorter.first_rel_index < self.generic_date[0] < self.sorter.last_rel_index:
                                self.is_valid_search = False
                                self.error_code = -3
                                return
                            # must be a valid specific date
                            else:
                                # make range just that day
                                self.start_rel_index = self.generic_date[0]
                                self.end_rel_index = self.generic_date[0]
                                # reset generic so we know not to check that
                                self.generic_date = []

                    #  start date must be <= end date, otherwise invalid
                    if self.start_rel_index > self.end_rel_index:
                        self.is_valid_search = False
                        self.error_code = -2
                        return

                    # don't add any keywords as search clauses
                    add_search_clause = False

                # change level of search
                elif search_word[:self.lvl_len] == self.lvl:
                    # keep track of which keyword could cause an error
                    self.keyword_error = self.lvl

                    if search_word[self.lvl_len:] == '0':
                        # normal search of whole day
                        self.level = 0
                    elif search_word[self.lvl_len:] == '1':
                        # all words have to be in one ptr
                        self.level = 1
                    else:
                        self.is_valid_search = False
                        self.error_code = -2
                        return

                    # don't add any keywords as search clauses
                    add_search_clause = False

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

                else:
                    search_clause = search_word

            # not a special search so just add
            else:
                search_clause = search_word

            if add_search_clause:
                # no repeats except for &&
                if search_clause == '&&':
                    if not last_clause_dup:  # don't add && if word before was a duplicate
                        self.search_clauses.append(search_clause)
                elif search_clause not in self.search_clauses:  # add and mark last as not a dup
                    self.search_clauses.append(search_clause)
                    last_clause_dup = False
                elif search_clause in self.search_clauses:  # remove &&s before duplicate
                    while self.search_clauses[-1] == '&&':
                        self.search_clauses.pop()
                    last_clause_dup = True

            i += 1

        # remove leading and trailing &&
        if self.search_clauses:
            while self.search_clauses[0] == '&&':
                self.search_clauses.pop(0)
            while self.search_clauses[-1] == '&&':
                self.search_clauses.pop()

            for i, clause in enumerate(self.search_clauses):
                if clause != '&&':
                    self.actual_search_clauses.append(i)

        self.is_valid_search = True

    # search through days to find finds and save indicies
    def do_search(self):
        for day_i in range(self.start_rel_index, self.end_rel_index + 1):  # only search desired range
            day: Day = self.sorter.days[self.sorter.rel_index_to_user_days(day_i)]

            # if just searching a date without clauses
            if not self.search_clauses:
                # first check if it matches the generic date (if we have)
                if self.generic_date:
                    if not day.is_match_generic_date(self.generic_date, self.sorter.is_euro_date):
                        continue

                # either matches or no generic date so output whole day
                self.finds_day_is.append(day_i)
                self.finds_is.append([-1])  # dummy value because we show whole day
                continue

            is_find: bool = self.do_lvl_search(day, day_i)

            # only sort and remove dups once for efficiency
            if is_find:
                self.finds_is[-1] = sorted(list(set(self.finds_is[-1])))
                is_find = False

        self.num_days_find = len(self.finds_day_is)
        self.num_finds = len(self.finds_is)

    def do_lvl_search(self, day: Day, day_i: int) -> bool:
        running_count_and_finds: int = 0  # count number of consecutive finds (to remove previous finds if &&)
        consec_and_clauses: int = 0  # count number of consecutive clauses in && run
        actaul_search_clauses_day: list[str] = self.actual_search_clauses  # clauses actually found on day
        is_last_clause_and: bool = False  # keep track of and logic in search
        is_last_clause_found: bool = False
        is_find: bool = False  # track if there are finds on the given day
        for i, clause in enumerate(self.search_clauses):
            # clause to left and right both must be finds
            if clause == '&&':
                is_last_clause_and = True
                consec_and_clauses += 1
                continue

                # EXCLUDEE ANDS FROM SEARCH THAT DONT HIT
                # IE ONLY INCLUDE HITS

            if is_last_clause_and:
                # if last clause before and was not found, remove and skip
                if not is_last_clause_found:
                    actaul_search_clauses_day.pop(actaul_search_clauses_day.index(i))
                    # reset as no longer careabout consecutiveness
                    consec_and_clauses = 0
                    is_last_clause_and = False
                    continue

            # if there is a generic date, check if it matches the generic date
            if self.generic_date:
                if not day.is_match_generic_date(self.generic_date, self.sorter.is_euro_date):
                    break  # go to next day

            # get all indicies in the day's ptrs that have the clause
            new_finds = [find_i for find_i, ptr in enumerate(day.ptrs) if self.search_clause_combos(clause, ptr)]

            if new_finds:
                if not is_find:  # first find on day
                    self.finds_day_is.append(day_i)
                    self.finds_is.append(new_finds)
                    is_find = True  # mark as found
                else:  # not first find (just add indicies, not day)
                    if self.level:  # we want every clause in a single pointer
                        # check overlap of self.find_is and new_finds to make sure we have repeats
                        repeat_finds = [find for find in self.finds_is[-1] if find in new_finds]
                        if not repeat_finds:  # no repeats = clause not found in same ptr = remove
                            self.finds_day_is.pop()
                            self.finds_is.pop()
                            return False
                        self.finds_is[-1] = repeat_finds  # only add repeats
                    else:
                        self.finds_is[-1] = self.finds_is[-1] + new_finds

                # only increment if last clause and
                # ie, only want to remove consecutive ands
                if running_count_and_finds < 1 or is_last_clause_and:
                    running_count_and_finds += len(new_finds)  # increment running count of finds found in && run

                is_last_clause_found = True
            else:
                if self.level:   # we want every clause in a single pointer
                    if is_find:  # have we found something yet
                        # get rid of previous finds
                        self.finds_day_is.pop()
                        self.finds_is.pop()
                    return False  # no finds

                # remove previous finds because one wasn't found
                # eg, a && b && c -> if a & b are both found, but c is not we remove a & b
                if is_last_clause_and:
                    # remove all finds that were added since and
                    for j in range(running_count_and_finds):
                        self.finds_is[-1].pop()

                        # if we remove all finds, completely remove
                        if not self.finds_is[-1]:
                            self.finds_day_is.pop()
                            self.finds_is.pop()
                            is_find = False

                    # reset as we just remoed all
                    running_count_and_finds = 0

                # if nothing found, remove the clause and all preceding clauses in && run
                index = actaul_search_clauses_day.index(i)
                actaul_search_clauses_day = (actaul_search_clauses_day[:max(0, index - consec_and_clauses)] +
                                             actaul_search_clauses_day[index + 1:])
                consec_and_clauses = 0  # reset as no longer careabout consecutiveness

                # reset back to 0 because last not found
                is_last_clause_found = False

                # last clause no longer &&
                is_last_clause_and = False

        # only search valid finds
        if is_find:
            self.finds_actual_clauses.append(actaul_search_clauses_day)

        return is_find

    def get_search_error_output(self):
        if self.error_code == -1:
            return Output.syntax_error_o
        elif self.error_code == -2:
            return Output.keyword_error_o
        elif self.error_code == -3:
            return Output.date_range_error_o

    # search the various types of hashers we want to look for
    def search_clause_combos(self, clause: str, ptr: str) -> bool:
        # hasher
        if clause[0] == '\\':
            # set context = 0 if hasher
            self.context = 0

            hasher = clause[1:]
            return ptr.startswith(hasher + ' ') or (' ' + hasher + ' ') in ptr or ('(' + hasher + ' ') in ptr
        return clause in ptr
