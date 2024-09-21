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

    def __init__(self, ptr):
        self.ptrs = []

        self.max_width = 100
        self.align_up_to = 4
        self.all_the_way = 6

        # split into each word
        words = ptr.split()
        date = words.pop(0).split('/')

        self.day = int(date[0])
        self.month = int(date[1])
        self.year = int(date[2])
        self.date_obj = datetime(self.year, self.month, self.day)
        self.day_of_week = self.date_obj.weekday()

        # get rid of ::
        words.pop(0)

        temp = ''
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

    # print date info nicely
    def print_date(self, lang: int):
        print(
            f'({self.days_of_week[lang][self.day_of_week]}) {self.day} {self.months[lang][self.month]}, {self.year}:')

    def has_ptrs(self):
        return self.ptrs

    # print all ptrs of a day
    def print_all_ptrs(self, lang: int):
        self.print_date(lang)

        if len(self.ptrs) == 0:
            # print aligned index
            print(f'{-1:>{self.align_up_to}}.', end=' ')
            print(f'{Output.empty_o[lang]:<{self.align_up_to}}')

        for index, element in enumerate(self.ptrs):
            # print aligned index
            print(f'{index:>{self.align_up_to}}.', end=' ')

            words = element.split()  # split into individual words
            no_overflow = ''  # store one line
            indent = ''  # for nice spacing for non-first lines (the < needs it)
            for token in words:
                if (len(no_overflow) + len(token)) > self.max_width:
                    if no_overflow:
                        print(f'{indent}{no_overflow:<{self.align_up_to}}')
                        indent = ' ' * (self.align_up_to + 2)

                    # check if it's a really long word and needs to be hyphenated
                    long_token, indent = self.handle_long_word(token, indent)

                    # add overflow word (either og word or end of super long) to next line
                    no_overflow = long_token

                else:
                    # add tokens to line
                    no_overflow += token

                # add space if not last word
                if token != words[-1]:
                    no_overflow += ' '

            # print rest of ptr if section doesn't overflow
            print(f'{indent}{no_overflow:<{self.align_up_to}}')

        print()

    # in case super long word, break down and hyphenate
    def handle_long_word(self, long_token: str, indent: str):
        while len(long_token) > self.max_width:
            hyphenated = long_token[:self.max_width - 1] + '-'
            print(f'{indent}{hyphenated:<{self.align_up_to}}')

            # no longer first line so align nicely (+2 for the dot and space)
            indent = ' ' * (self.align_up_to + 2)
            long_token = long_token[self.max_width:]

        return long_token, indent

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
                return (comp_date-start.date_obj).days
            return -1
        except ValueError:
            # invalid date
            return -1

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
