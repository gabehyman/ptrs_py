import os
from day import Day
from output import Output
from datetime import datetime, timedelta


class User:
    always_ops = ['t', 'mm', 'tt']

    def __init__(self):
        self.wd: str = os.path.dirname(os.path.realpath(__file__))
        self.user_path: str = self.wd + '/user.txt'
        self.ptrs_path: str = self.wd + '/ptrs.txt'

        self.lang: int = 0
        self.name: str = ''

    def pos_handler(self, cur_pos: str, mod: str):
        if mod == '-1':
            return cur_pos[:-1]
        if mod == '-2':
            return '_'
        if mod == '-3':
            return ''

        return cur_pos + mod

    def input_handler(self, prompt: list[str], cur_pos: str = ''):
        num_inputs = int(prompt[-1])
        while True:
            user_input: str = input(prompt[self.lang] + '\n')
            print()  # extra line below answer

            if user_input == '':  # hit enter for last op
                if num_inputs == 0:  # unless we need an answer
                    self.just_print_i(Output.no_empty_o)
                    continue
                # if they ask for another random day at start, no change
                elif cur_pos == '_':
                    return cur_pos
                return self.pos_handler(cur_pos, str(num_inputs - 1))

            # num_inputs = 0 -> need non-empty answer (no always ops available)
            # actual num of inputs then is 2nd to last option
            if num_inputs == 0:
                real_num_inputs = int(prompt[-2])
                if (real_num_inputs == -1 or  # take any response
                        (user_input.isdigit() and  # make sure its a number b4 forcing below
                         int(user_input) in range(real_num_inputs))):  # in valid range
                    return user_input
            else:
                # check always ops
                for i in range(len(self.always_ops)):
                    if user_input.lower() == self.always_ops[i]:
                        return self.pos_handler(cur_pos, str(-i - 1))

                # _________ = -1 -> can just write ptrs but can also pick option
                if num_inputs == -1:
                    # 2nd to last element will tell nums ops
                    if int(user_input) in range(int(prompt[-2])):
                        return self.pos_handler(cur_pos, user_input)
                    else:
                        return user_input

                # find op
                if int(user_input) in range(num_inputs):
                    return self.pos_handler(cur_pos, user_input)

            # no match, say invalid and re-run
            self.just_print_i(Output.invalid_o)

    def create_user(self):
        with open(self.user_path, 'w') as file:  # create user file
            # take language pref and write to file
            self.lang = int(self.input_handler(Output.language_o))
            file.write(str(self.lang) + '\n')

            # take name and write to file
            self.name = self.input_handler(Output.name_o)
            file.write(self.name + '\n')

        with open(self.ptrs_path, 'w') as file:  # create file
            # create ptrs file with 20 days both in past and future
            current_date = datetime.now()
            back_forth = 20
            for i in range(-back_forth, back_forth):
                date = current_date + timedelta(days=i)
                month = Day.months[self.lang][date.month - 1]
                file.write(f'{date.day} {month}, {date.year} ::  \t\n')

    def user_info(self):
        wd = os.path.dirname(os.path.realpath(__file__))

        user_path = wd + '/user.txt'
        if not (os.path.exists(user_path)):
            self.create_user()
            return

        info = []
        with open(user_path, 'r') as file:
            for line in file:
                info.append(line.strip())

        self.lang = int(info[0])
        self.name = info[1]

    def just_print_i(self, output_all, with_name: int = 0):
        printer = output_all[self.lang]

        if with_name:
            printer += self.name

        printer += '.'

        print(printer)

    def get_cur_pos(self, pos, outputter):
        cur_pos = 'pos_o' + pos

        return getattr(outputter, cur_pos)
