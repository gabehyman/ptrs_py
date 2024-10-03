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

    def __init__(self, ptr):
        self.ptrs: list[str] = []

        self.max_width: int = 100
        self.align_up_to_ptr: int = 3
        self.align_up_to_day: int = 4

        # split into each word
        words: list[str] = ptr.split()
        date: list[str] = words.pop(0).split('/')

        self.day: int = int(date[0])
        self.month: int = int(date[1])
        self.year: int = int(date[2])
        self.date_obj: datetime = datetime(self.year, self.month, self.day)

        # how many days since aug 24, 1999
        self.rel_index: int = (self.date_obj - Day.start_of_time).days

        # 0 = mon 6 = sun
        self.day_of_week: int = self.date_obj.weekday()

        # get rid of ::
        words.pop(0)

        temp: str = ''
        for token in words:
            temp += token
            if ',' in token:
                self.ptrs.append(temp[:-1])  # add without comma
                temp = ''  # reset temp
            else:
                temp += ' '  # add a space after each word

        # add remaining text in temp to pointers
        if temp:
            if ',' in temp:
                temp = temp[:-1]
            self.ptrs.append(temp.strip())

        self.num_ptrs = len(self.ptrs)

    # print date info nicely
    def get_nice_date(self, lang: int) -> str:
        return (
            f'({self.days_of_week[lang][self.day_of_week]}) {self.day} {self.months[lang][self.month]}, {self.year}:')

    def has_ptrs(self):
        return self.ptrs

    # print all ptrs of a day
    def print_all_ptrs(self, lang: int):
        Day.print_with_div(self.get_nice_date(lang))

        if self.num_ptrs == 0:
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

    def print_search_ptrs(self, lang: int, num_day: int, find_is: list[int], search_clauses: list[str], context: int):
        # print aligned index
        Day.print_with_div(f'{Day.num_to_letter(num_day):>{self.align_up_to_day}}. {self.get_nice_date(lang)}')

        for i in self.get_context_search_indicies(find_is, context):
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

    def get_context_search_indicies(self, find_is: list[int], context: int) -> list[int]:
        context_is: set = set()
        for find_i in find_is:
            # get range of start and end of context
            start = max(0, find_i - context)
            end = min(self.num_ptrs - 1, find_i + context)

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

    def is_match_generic_date(self, dmy: list[str], is_euro_date: bool) -> bool:
        match: bool = False
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

    @staticmethod
    def find_all_substring_is(ptr: str, search_clauses: list[str]) -> (list[int], list[int]):
        start_is: set = set()
        end_is: set = set()

        for clause in search_clauses:
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

    @staticmethod
    def highlight_finds(ptr: str, start_is: list[int], end_is: list[int]) -> str:
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
                ptr_list.insert(start_is[counter_start], '*')
                counter_start += 1
            else:
                ptr_list.insert(end_is[counter_end] + 1, '*')
                counter_end += 1

        return ''.join(ptr_list)

    @staticmethod
    def print_with_div(output: str, name: str = '', before: bool = True, after: bool = True, char: chr = '-'):
        if name:
            output += f',{name}.'

        if before:
            print(char * len(output))
        print(output)
        if after:
            print(char * len(output))

    @staticmethod
    def num_to_letter(num: int) -> str:
        base = 26  # numm letters in alphabet
        remainder = num % base
        div = num // base

        # 'a'= 97 in ascii
        return chr(remainder + 97) * (div + 1)

    # handle euro and american dates
    @staticmethod
    def sort_dmy(dmy, is_euro_date: bool):
        if is_euro_date:
            # 24aug 1999
            return dmy[0], dmy[1], dmy[2]
        # aug24 1999
        return dmy[1], dmy[0], dmy[2]

    @staticmethod
    def date_to_index(date_str: str, is_euro_date: bool, is_range: bool = False):
        date_obj: datetime
        d_format = "%d/%m/%y"
        if not is_euro_date:
            d_format = "%m/%d/%y"

        try:
            # first try a two digit year
            date_obj = datetime.strptime(date_str, d_format)
        except ValueError:
            try:
                # then a four digit year
                date_obj = datetime.strptime(date_str, d_format)
            except ValueError as e:
                if is_range:
                    return -2
                else:
                    dmy = date_str.split('/')
                    if len(dmy) != 3:
                        return -2

                    all_empty = 0
                    for part in dmy:
                        if not part.isdigit():
                            if part:
                                return -2
                        elif part:
                            all_empty += 1

                    # can't have all empty (///) or all numbers (cuz shouldve been valid with datetime)
                    if all_empty == 0:
                        return -2

                    day = 0
                    month = 0
                    year = 4

                    day_search, month_search, year_search = Day.sort_dmy(dmy, is_euro_date)

                    # month has to be 1-12
                    if month_search:
                        month = int(month_search)
                        if not 0 < month <= 12:
                            return -2

                    # year must be same/after start_of_time
                    if year_search:
                        year = int(year_search)

                        # can't be before start of time
                        if 0 < year < Day.start_of_time.year:
                            return -3
                        elif (year == Day.start_of_time.year and
                              month < Day.start_of_time.year):
                            return -3

                    # if we have a day and month, we need to check if day is valid
                    if day_search:
                        day = int(day_search)
                        if not 0 < day < 31:
                            return -2
                        elif month != 0:
                            try:
                                # see if valid date in a leap year (= 4) or given year
                                datetime(year, month, day)

                                # can't be before start of time
                                if (year == Day.start_of_time.year and
                                        (month == Day.start_of_time.year and
                                         day < Day.start_of_time.day)):
                                    return -3
                            except ValueError:
                                return -2

                    # just to include leap year
                    if year == 4:
                        year = 0
                    return day, month, year

        # can't do anything before start of time
        if date_obj < Day.start_of_time:
            return -3

        return (date_obj - Day.start_of_time).days

    @staticmethod
    def get_dates_around_today(delta):
        current_date = datetime.now()
        date = current_date + timedelta(days=delta)
        return date.day, date.month, date.year

    @staticmethod
    def make_date(day, month, year):
        try:
            return datetime(int(year), int(month), int(day))
        except ValueError:
            # if invalid date return date at beginning of time haha
            return datetime(1, 1, 1)

    @staticmethod
    def get_index(start, end, day, month, year):
        try:
            comp_date = datetime(int(year), int(month), int(day))
            if start.date_obj <= comp_date <= end.date_obj:
                return (comp_date - start.date_obj).days
            return -2  # date out of range of ptrs
        except ValueError:
            return -3  # invalid date

    # check if input is one of the months first three letters (english)
    @staticmethod
    def is_three_letter_month(mth: str) -> int:
        counter = 1
        if len(mth) == 3:
            for month in Day.months[0]:
                if mth == month[:3]:
                    return counter
                counter += 1
        return -1

    # check if input is one of the days of weeks first three letters (english)
    @staticmethod
    def is_three_letter_day(usr_day: str) -> int:
        counter = 0
        if len(usr_day) == 3:
            for day in Day.days_of_week[0]:
                if usr_day == day[:3]:
                    return counter
                counter += 1
        return -1
