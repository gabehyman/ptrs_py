import os
from day import Day
from output import Output


class User:
    always_ops = ['t', 'mm', 'tt']

    def __init__(self):
        self.wd: str = os.path.dirname(os.path.realpath(__file__))
        self.user_path: str = self.wd + '/user.txt'
        self.ptrs_path: str = self.wd + '/ptrs.txt'

        self.lang: int = 0
        self.name: str = ''

        self.cur_in: str = ''
        self.cur_pos: str = ''

        self.has_searched: bool = False

        if not (os.path.exists(self.ptrs_path)):
            self.create_ptrs_file()
        if not (os.path.exists(self.user_path)):
            self.cur_pos = "_"  # prompt user info
            self.already_user = False
        else:
            self.set_user_info()
            self.cur_pos = '___'

            # nice spacing
            Day.print_with_div(self.get_lang_spec_output(Output.welcome_o), self.name, char='*')
            print()
            self.already_user = True

        # TODO: make a switch for this in user.txt
        # handle european and american date formats
        self.is_euro_date = True
        self.user_edit_in_prog: bool = False

    def create_ptrs_file(self):
        with open(self.ptrs_path, 'w') as file:  # create file
            # create ptrs file with 20 days both in past and future
            back_forth = 20
            for i in range(-back_forth, back_forth):
                day, month, year = Day.get_dates_around_today(i)
                file.write(f'{day}/{month}/{year} ::  \t\n')

    def set_user_info(self):
        with open(self.user_path, 'r') as file:
            self.lang = int(next(file).strip())
            self.name = next(file).strip()

    def update_user(self):
        with open(self.user_path, 'w') as file:  # create user file
            file.write(str(self.lang) + '\n')
            file.write(self.name + '\n')

        # nice spacing
        Day.print_with_div(self.get_lang_spec_output(Output.welcome_new_o), self.name, char='*')
        print()

        self.user_edit_in_prog = False

    def is_user_info_changed(self) -> bool:
        if not (os.path.exists(self.user_path)):
            return True

        with open(self.user_path, 'r') as file:
            lang_t = int(next(file).strip())
            name_t = next(file).strip()

            if lang_t != self.lang or name_t != self.name:
                return True

        return False

    def pos_handler(self, mod: int):
        # go back one (t)
        if mod == -1:
            self.cur_pos = self.cur_pos[:-1]
            return

        # go back to main menu (mm)
        elif mod == -2:
            if self.already_user:
                self.cur_pos = Output.all_pos_names_o['mm']
                self.has_searched = False  # clear searcher
                return

            # mm not available without preferences
            print(self.get_lang_spec_output(Output.mm_unavailable_o))
            return

        # end program (tt)
        elif mod == -3:
            self.cur_pos = ''
            return

        # handle normally
        self.cur_pos += str(mod)

    def input_handler(self, prompt: list[str | int], dyn_num_inputs: int):
        # keep type of prompt if actual num_inputs is different (<0)
        num_inputs_type = prompt[-1]
        num_inputs = prompt[-1]
        if num_inputs == 1:
            num_inputs = dyn_num_inputs
        elif num_inputs_type < 0:
            num_inputs = prompt[-2]

        while True:
            user_input: str = input(prompt[self.lang] + '\n')
            print()  # extra line below answer

            # remove empty spaces
            self.cur_in = user_input.strip()

            # check always ops
            if self.check_always_op_and_update():
                return

            # hit enter for last op
            if self.cur_in == '':
                if num_inputs_type == 0 or num_inputs_type == 1:  # unless we need an answer
                    print(self.get_lang_spec_output(Output.no_empty_o))
                    continue
                elif num_inputs_type == -1:  # auto next and save pos info in cur_in
                    self.auto_next_pos()
                    self.cur_in = str(num_inputs - 1)  # last option
                    return

                # handle normal case OR where they can check range + in = out
                self.pos_handler(num_inputs - 1)
                return

            # input = output (auto next, can't be empty)
            elif num_inputs == 0:
                self.auto_next_pos()
                return

            # all remaining ops have range check
            # check if type = -1 to auto next instead of move to actual option
            elif self.check_valid_range_and_update(num_inputs, num_inputs_type):
                return

            # either in = out (specific pos) OR normal range check
            # and just checked range above so must be in = out
            if num_inputs_type == -2:
                self.pos_handler(0)  # in = out will be the 0th option
                return

            # no match, say invalid and re-run
            print(self.get_lang_spec_output(Output.invalid_o))

    # only one prompt/level that could be next
    def auto_next_pos(self):
        self.cur_pos += '_'

    def check_valid_range_and_update(self, num_inputs: int, auto_next_type: int = 0) -> bool:
        if self.cur_in.isdigit():  # make sure its a number b4 forcing below
            cur_in_i = int(self.cur_in)
            if cur_in_i < num_inputs:  # also will return false for neg nums
                if auto_next_type == -1 or auto_next_type == 1:
                    self.auto_next_pos()
                else:
                    self.pos_handler(cur_in_i)
                return True
        return False

    # check always ops
    def check_always_op_and_update(self) -> bool:
        for i in range(len(self.always_ops)):
            if self.cur_in == self.always_ops[i]:
                self.pos_handler(-i - 1)
                return True

        # not an always op
        return False

    def get_lang_spec_output(self, output_all):
        return output_all[self.lang]

    def search_error_addendum(self, search_params) -> str:
        if search_params[0] == '-1':
            return self.get_lang_spec_output(Output.syntax_error_o) + search_params[1]
        elif search_params[0] == '-2':
            return self.get_lang_spec_output(Output.date_range_error_o)
        elif search_params[0] == '-3':
            return self.get_lang_spec_output(Output.date_range_error_o)
