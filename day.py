from output import Output

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
        self.day: int = 0
        self.month: int = 0
        self.year: int = 0
        self.ptrs = []

        self.max_width = 100
        self.align_up_to = 4
        self.all_the_way = 6

        # split into each word
        words = ptr.split()

        self.day = int(words.pop(0))

        month_s = words.pop(0)[:-1]

        # check all langs, maybe ptrs in diff lang than ui
        # dev purposes??
        for month_lang in self.months:
            if month_s in month_lang:
                self.month = int(month_lang.index(month_s))
                break

        self.year = int(words.pop(0))

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
            f'({self.days_of_week[lang][self.getDayOfWeek()]}) {self.day} {self.months[lang][self.month]}, {self.year}:')

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

    def getDayOfWeek(self):
        # zeller's congruence
        k = self.year % 100
        j = self.year // 100
        h = (self.day + ((13 * (self.zeller_month(self.month) + 1)) // 5) + k + k // 4 + j // 4 + 5 * j)

        return ((h % 7) + 5) % 7  # have it match with mon - sun indexing

    def zeller_month(self, month_index):
        return ((month_index + 1) + 9) % 12 + 3
