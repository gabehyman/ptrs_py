from output import Output

from datetime import datetime, timedelta


class Day:
    days_of_week: list[list[str]] = [['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                                     ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'],
                                     ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']]
    months: list[list[str]] = [
        ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
         'december'],
        ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
         'deciembre'],
        ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november',
         'december']]
    # arbitrary (kinda) start of time
    start_of_time: datetime = datetime(1999, 8, 24)

    # spacing vars
    max_width: int = 100
    align_up_to_ptr: int = 4
    align_up_to_day: int = 6

    def __init__(self, ptrs: str, rel_index: int):
        self.ptrs: list[str] = Day.csv_ptrs_to_list(ptrs)
        self.date_obj = Day.rel_index_to_date(rel_index)
        self.rel_index: int = rel_index  # how many days since aug 24, 1999

        self.day: int = self.date_obj.day
        self.month: int = self.date_obj.month
        self.year: int = self.date_obj.year
        self.day_of_week: int = self.date_obj.weekday()  # 0 = mon 6 = sun

    # print date info nicely
    def get_nice_date(self, lang: int, is_euro_date: bool) -> str:
        if is_euro_date:
            return (
                f'({self.days_of_week[lang][self.day_of_week]}) {self.day} {self.months[lang][self.month - 1]}, {self.year}:')

        return (
            f'({self.days_of_week[lang][self.day_of_week]}) {self.months[lang][self.month - 1]} {self.day}, {self.year}:')

    def has_ptrs(self) -> bool:
        return bool(self.ptrs)

    # print all ptrs of a day
    def print_all_ptrs(self, lang: int, is_euro_date: bool):
        Day.print_with_div(self.get_nice_date(lang, is_euro_date))

        if len(self.ptrs) == 0:
            # print aligned index
            print(f'{-1:>{self.align_up_to_ptr}}.', end=' ')
            print(f'{Output.empty_o[lang]:<{self.align_up_to_ptr}}')

        for i, ptr in enumerate(self.ptrs):
            # print aligned index
            print(f'{i:>{self.align_up_to_ptr}}.', end=' ')

            words = ptr.split()  # split into individual words
            no_overflow = ''  # store one line
            indent = ''  # for nice spacing for non-first lines (the < needs it)
            for word in words:
                if (len(no_overflow) + len(word)) > self.max_width:
                    if no_overflow:
                        print(f'{indent}{no_overflow:<{self.align_up_to_ptr}}')
                        indent = ' ' * (self.align_up_to_ptr + 2)

                    # check if it's a really long word and needs to be hyphenated
                    long_token, indent = self.handle_long_word(word, indent)

                    # add overflow word (either og word or end of super long) to next line
                    no_overflow = long_token

                else:
                    # add tokens to line
                    no_overflow += word

                # add space if not last word
                if word != words[-1]:
                    no_overflow += ' '

            # print rest of ptr if section doesn't overflow
            print(f'{indent}{no_overflow:<{self.align_up_to_ptr}}')

        print()

    def print_search_ptrs(self, lang: int, num_day: int, find_is: list[int], search_clauses: list[str], context: int,
                          is_euro_date: bool):
        # print aligned index only if more than one day
        # num_day passed in = -1 if only one day
        day_num_pound = ''
        find_is_foo = find_is
        if num_day != -1:
            # show number next to day for search if more than 1 day
            pound_num_day = f'#{str(num_day)}'
            day_num_pound = f'{pound_num_day:>{self.align_up_to_day}}. '
        else:
            find_is_foo = [-1]  # print all ptrs in day if only 1 day
        Day.print_with_div(f'{day_num_pound}{self.get_nice_date(lang, is_euro_date)}')

        for i in self.get_context_search_indicies(find_is_foo, context):
            no_overflow = ''  # store one line
            ptr = self.ptrs[i]  # store ptr
            if i in find_is:  # indicate line with find
                no_overflow = '--> '

                start_is, end_is = Day.find_all_substring_is(ptr, search_clauses)
                ptr = Day.highlight_finds(ptr, start_is, end_is)

            # print aligned index
            print(f'{i:>{self.align_up_to_ptr}}.', end=' ')

            words = ptr.split()  # split into individual words
            indent = ''  # for nice spacing for non-first lines (the < needs it)
            for j, word in enumerate(words):
                if (len(no_overflow) + len(word)) > self.max_width:
                    if no_overflow:
                        print(f'{indent}{no_overflow:<{self.align_up_to_ptr}}')
                        indent = ' ' * (self.align_up_to_ptr + 2)

                    # check if it's a really long word and needs to be hyphenated
                    long_token, indent = self.handle_long_word(word, indent)

                    # add overflow word (either og word or end of super long) to next line
                    no_overflow = long_token

                else:
                    # add tokens to line
                    no_overflow += word

                # add space if not last word
                if j != len(words) - 1:
                    no_overflow += ' '

            # print rest of ptr if section doesn't overflow
            print(f'{indent}{no_overflow:<{self.align_up_to_ptr}}')

        print()

    def get_context_search_indicies(self, find_is: list[int], context: int) -> list[int]:
        # pass in find_is = [-1] if you want all
        if find_is[0] == -1:
            return range(len(self.ptrs))

        context_is: set = set()
        for find_i in find_is:
            # get range of start and end of context
            start = max(0, find_i - context)
            end = min(len(self.ptrs) - 1, find_i + context)

            # add range to set
            context_is.update(range(start, end + 1))

        return sorted(context_is)  # Convert to a sorted list before returning

    # in case super long word, break down and hyphenate
    def handle_long_word(self, long_token: str, indent: str):
        while len(long_token) > self.max_width:
            hyphenated = long_token[:self.max_width - 1] + '-'
            print(f'{indent}{hyphenated:<{self.align_up_to_ptr}}')

            # no longer first line so align nicely (+2 for the dot and space)
            indent = ' ' * (self.align_up_to_ptr + 2)
            long_token = long_token[self.max_width:]

        return long_token, indent

    def is_match_generic_date(self, dmy: list[int], is_euro_date: bool) -> bool:
        day, month, year = Day.sort_dmy(dmy, is_euro_date)
        if day:
            if self.day != day:
                return False
        if month:
            if self.month != month:
                return False
        if year:
            if self.year != year:
                return False
        return True

    # convert all ptrs into a csv string
    def get_all_ptrs_csv(self) -> str:
        all_ptrs_csv: str = ''
        # return empty str if no ptrs
        if self.has_ptrs():
            # all ptrs comma seperated, no comma at end
            for ptr in self.ptrs[:-1]:
                all_ptrs_csv += ptr
                all_ptrs_csv += ', '
            all_ptrs_csv += self.ptrs[-1]

        return all_ptrs_csv

    # write the ptrs file and update the program data
    def write_ptrs(self, ptrs_str: str, ptr_folder_path, ptrs_file_name, append: bool = False):
        day_ptr_path = ptr_folder_path + str(self.rel_index) + ptrs_file_name

        # only append if we already have ptrs
        if self.has_ptrs() and append:
            ptrs_str = self.get_all_ptrs_csv() + ', ' + ptrs_str

        # synch program ptr
        self.ptrs = Day.csv_ptrs_to_list(ptrs_str)
        with open(day_ptr_path, 'w') as file:
            # ensure nice formatting
            file.write(self.get_all_ptrs_csv())

    # turn csv str ptrs to a list
    @staticmethod
    def csv_ptrs_to_list(ptr: str) -> list[str]:
        # return empty list if empty ptrs
        if not ptr:
            return []

        # no leading/trailing spaces and split at comma
        # (not comma + space to handle varied input (all backend is comma + space)
        ptrs_unstripped: list[str] = ptr.split(',')
        return [ptr.strip() for ptr in ptrs_unstripped]

    # find start and end indicies of all actual search clauses (to put ** around find)
    @staticmethod
    def find_all_substring_is(ptr: str, actual_search_clauses: list[str]) -> (list[int], list[int]):
        start_is: set = set()
        end_is: set = set()

        for clause in actual_search_clauses:
            # start from the beginning
            start_i = ptr.find(clause)

            while start_i != -1:
                end_i = start_i + len(clause) - 1
                start_is.add(start_i)
                end_is.add(end_i)

                # move search forward
                start_i = ptr.find(clause, start_i + 1)

        # reverse so we can start at end and not mess up indicies before
        return [sorted(start_is, reverse=True), sorted(end_is, reverse=True)]

    # add ** around finds
    @staticmethod
    def highlight_finds(ptr: str, start_is: list[int], end_is: list[int]) -> str:
        highlighter = '*'

        # tokenize
        ptr_list = list(ptr)
        counter_start = 0
        counter_end = 0
        # make sure in bounds of at least one array
        while counter_start < len(start_is) or counter_end < len(end_is):
            insert_start = False  # add start i or end i
            if counter_start < len(start_is):
                if counter_end < len(end_is):
                    if start_is[counter_start] >= end_is[counter_end]:
                        insert_start = True
                else:
                    insert_start = True

            # just do adding here to consolidate
            # pick the bigger (or available) one, insert * and increment
            if insert_start:
                ptr_list.insert(start_is[counter_start], highlighter)
                counter_start += 1
            else:
                ptr_list.insert(end_is[counter_end] + 1, highlighter)
                counter_end += 1

        return ''.join(ptr_list)

    # print nice divider in console
    @staticmethod
    def print_with_div(output: str, name: str = '', before: bool = True, after: bool = True, char: chr = '-'):
        if name:
            output += f', {name}.'

        if before:
            print(char * len(output))
        print(output)
        if after:
            print(char * len(output))

    # handle euro and american dates
    @staticmethod
    def sort_dmy(dmy: list[int], is_euro_date: bool) -> list[int]:
        if is_euro_date:
            # 24aug 1999
            return dmy
        # aug24 1999
        return [dmy[1], dmy[0], dmy[2]]

    # convert relative index to a date (eg, 7599 to 13jun20)
    @staticmethod
    def rel_index_to_date(rel_index):
        date = Day.start_of_time + timedelta(days=rel_index)
        return date

    # turn a user inputted date into a 3 valued list date (d/m/y or m/d/y)
    @staticmethod
    def date_to_index(date_str: str, is_euro_date: bool, is_range: bool = False) -> list[int]:
        date_obj: datetime
        d_format = '%d/%m/%Y'
        if not is_euro_date:
            d_format = '%m/%d/%Y'

        # check if three letter date and convert
        date_str = Day.three_letter_date_to_dmy(date_str, is_euro_date)

        try:
            # first try a four digit year
            date_obj = datetime.strptime(date_str, d_format)
        except ValueError:
            try:
                # then a four digit year
                d_format = d_format[:-1] + 'y'
                date_obj = datetime.strptime(date_str, d_format)
            except ValueError as e:
                if is_range:
                    return [-2]
                else:
                    # if '/' not in date_str:
                    #     return [-2]
                    dmy = date_str.split('/')
                    if len(dmy) != 3:
                        return [-2]

                    all_empty = 0
                    for i in range(len(dmy)):
                        if not dmy[i].isdigit():
                            if dmy[i]:
                                return [-2]

                            # must be empty so add to count and make it 0
                            all_empty += 1
                            dmy[i] = '0'

                    # can't have all empty (///) or all numbers (cuz shouldve been valid with datetime)
                    if all_empty == 3 or all_empty == 0:
                        return [-2]

                    day_search, month_search, year_search = Day.sort_dmy([int(p) for p in dmy], is_euro_date)

                    day: int = 0
                    month: int = 0
                    year: int = 4  # include leap year

                    # month has to be 1-12
                    if month_search:
                        month = month_search
                        if not 0 < month <= 12:
                            return [-2]

                    # year must be same/after start_of_time
                    if year_search:
                        year = year_search

                        if year < 100:
                            # let datetime convert two digit year to four
                            year = datetime.strptime(f'1/1/{year}', d_format).year

                        # can't be before start of time
                        if 0 < year < Day.start_of_time.year:
                            return [-3]
                        elif (year == Day.start_of_time.year and
                              month < Day.start_of_time.month):
                            return [-3]

                    # if we have a day and month, we need to check if day is valid
                    if day_search:
                        day = day_search
                        if not 0 < day < 31:
                            return [-2]
                        elif month != 0:
                            try:
                                # see if valid date in a leap year (= 4) or given year
                                datetime(year, month, day)

                                # can't be before start of time
                                if (year == Day.start_of_time.year and
                                        (month == Day.start_of_time.month and
                                         day < Day.start_of_time.day)):
                                    return [-3]
                            except ValueError:
                                return [-2]

                    # just to include leap year
                    if year == 4:
                        year = 0
                    return [day, month, year]

        # can't do anything before start of time
        if date_obj < Day.start_of_time:
            return [-3]

        return [(date_obj - Day.start_of_time).days]

    # convert a three letter date input (24aug99) in to m/d/y (24/8/99)
    @staticmethod
    def three_letter_date_to_dmy(three_letter_date: str, is_euro_month: bool) -> str:
        # not a three letter date so just return original to process
        # also must be in euro month to use (can't do oct1224)
        if '/' in three_letter_date or not is_euro_month:
            return three_letter_date

        day: str = ''
        month: str = ''
        year: str = ''

        date_len = len(three_letter_date) - 1

        # find day
        start_i = 0
        while start_i <= date_len and three_letter_date[start_i].isdigit():
            start_i += 1

        # find year
        end_i = date_len
        while end_i >= 0 and three_letter_date[end_i].isdigit():
            end_i -= 1

        # find month
        three_letter_month = three_letter_date[start_i:3 + start_i]
        for i, mnth in enumerate(Day.months[0]):
            if three_letter_month == mnth[:3]:
                month = str(i + 1)
                break

        if month:
            if start_i:
                day = three_letter_date[0:start_i]
            if end_i != date_len:
                year = three_letter_date[end_i + 1:]

            if is_euro_month:
                return f'{day}/{month}/{year}'
            return f'{month}/{day}/{year}'

        return three_letter_date

    # get the relative index of day about the current day and a given delta
    @staticmethod
    def get_rel_index_dates_around_today(delta) -> int:
        current_date = datetime.now()
        date = current_date + timedelta(days=delta)
        return (date - Day.start_of_time).days
