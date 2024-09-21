import os
from day import Day
from output import Output


def is_valid_range(user_input, num_inputs):
    return (user_input.isdigit() and  # make sure its a number b4 forcing below
            int(user_input) in range(num_inputs))


class User:
    always_ops = ['t', 'mm', 'tt']

    def __init__(self):
        self.wd: str = os.path.dirname(os.path.realpath(__file__))
        self.user_path: str = self.wd + '/user.txt'
        self.ptrs_path: str = self.wd + '/ptrs.txt'

        self.lang: int = 0
        self.name: str = ''

    def pos_handler(self, cur_pos: str, mod: str):
        # go back one
        if mod == '-1':
            return cur_pos[:-1]
        # go back to start
        if mod == '-2':
            return '_'
        # end program
        if mod == '-3':
            return ''

        return cur_pos + mod

    def input_handler(self, prompt: list[str], cur_pos: str = ''):
        # keep track of non-positional returns
        dum_out = ''
        num_inputs = int(prompt[-1])
        while True:
            user_input: str = input(prompt[self.lang] + '\n')
            print()  # extra line below answer

            if user_input == '':  # hit enter for last op
                if num_inputs == 0:  # unless we need an answer
                    self.just_print(Output.no_empty_o)
                    continue
                return [self.pos_handler(cur_pos, str(num_inputs - 1)), dum_out]

            # num_inputs = 0 -> need non-empty answer
            # actual num of inputs then is 2nd to last option
            elif num_inputs == 0:
                num_inputs = int(prompt[-2])
                # always ops or valid range
                if num_inputs == -2:
                    # check always ops
                    pos_ret = self.find_always_op(user_input, cur_pos)
                    if pos_ret != '-1':
                        return [pos_ret, dum_out]
                    # check valid range
                    elif is_valid_range(user_input, num_inputs):
                        return [self.pos_handler(cur_pos, user_input), dum_out]
                    # if neither, return input
                    return [cur_pos, user_input]
                # return user input (if -1 (ie take anything) or in valid range)
                elif (num_inputs == -1 or
                        is_valid_range(user_input, num_inputs)):
                    return [cur_pos, user_input.strip()]
            else:
                # check always ops
                pos_ret = self.find_always_op(user_input, cur_pos)
                if pos_ret != '-1':
                    return [pos_ret, dum_out]

                # num_inputs = -1 -> can just write ptrs but can also pick option
                elif num_inputs == -1:
                    # 2nd to last element will tell nums ops
                    # check if valid op
                    num_inputs = int(prompt[-2])
                    if is_valid_range(user_input, num_inputs):
                        return [self.pos_handler(cur_pos, user_input), dum_out]
                    else:
                        return [cur_pos, user_input.strip()]

                # check valid op
                elif is_valid_range(user_input, num_inputs):
                    return [self.pos_handler(cur_pos, user_input), dum_out]

            # no match, say invalid and re-run
            self.just_print(Output.invalid_o)

    def find_always_op(self, user_input, cur_pos):
        # check always ops
        for i in range(len(self.always_ops)):
            if user_input.lower() == self.always_ops[i]:
                return self.pos_handler(cur_pos, str(-i - 1))

        # not an always op
        return '-1'

    def user_info(self):
        # get working dir
        wd = os.path.dirname(os.path.realpath(__file__))

        user_path = wd + '/user.txt'
        if not (os.path.exists(user_path)):
            self.create_user()
            self.just_print(Output.welcome_new_o, True, True)
            return

        info = []
        with open(user_path, 'r') as file:
            for line in file:
                info.append(line.strip())

        self.lang = int(info[0])
        self.name = info[1]

        self.just_print(Output.welcome_o, True, True)

    def create_user(self):
        with open(self.user_path, 'w') as file:  # create user file
            # take language pref and write to file
            self.lang = int(self.input_handler(Output.language_o)[1])
            file.write(str(self.lang) + '\n')

            # take name and write to file
            self.name = self.input_handler(Output.name_o)[1]
            file.write(self.name + '\n')

        with open(self.ptrs_path, 'w') as file:  # create file
            # create ptrs file with 20 days both in past and future
            back_forth = 20
            for i in range(-back_forth, back_forth):
                day, month, year = Day.get_dates_around_today(i)
                file.write(f'{day}/{month}/{year} ::  \t\n')

    def just_print(self, output_all, with_name: bool = False, with_div: bool = False):
        printer = output_all[self.lang]

        if with_name:
            printer += self.name

        printer += '.'

        if with_div:
            print(f'\n{Output.divider_o}')
        print(printer)
        if with_div:
            print(f'{Output.divider_o}\n')

    def repeat_prompt(self, pos):
        trunc_pos = pos[:-1]
        if trunc_pos in []: # Output.same_prompt:
            return trunc_pos + 'x'
        return pos
