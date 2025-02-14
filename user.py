import os
import json

from day import Day
from output import Output


class User:
    # t = back = -1 | mm = min menu = -2 | tt = end program = -3
    always_ops = ['t', 'mm', 'tt']

    def __init__(self):
        self.wd: str = os.path.dirname(os.path.realpath(__file__))
        self.user_path: str = self.wd + '/user.json'
        self.ptr_folder_path: str = self.wd + '/ptrs/'
        self.ptrs_file_name: str = '/ptrs.txt'

        # asnwered by user
        self.lang: int = 0
        self.is_euro_date: bool = True
        self.name: str = ''
        self.user_data = {}

        # track user input and position in program
        self.cur_in: str = ''
        self.cur_pos: str = ''
        self.prev_pos: str = ''

        # allow for user to go back to previous search result
        self.has_searched: bool = False

        if not (os.path.isdir(self.ptr_folder_path)):
            self.create_ptr_folders()
        if not (os.path.exists(self.user_path)):
            self.update_cur_pos(Output.all_pos_names_o['lang'])  # prompt user info
            self.already_user = False
        else:
            self.get_user_info()  # read from file
            self.update_cur_pos(Output.all_pos_names_o['mm'])

            # nice spacing
            Day.print_with_div(self.get_lang_spec_output(Output.welcome_o), self.name, char='*')
            print()
            self.already_user = True

        self.user_edit_in_prog: bool = False

    def create_ptr_folders(self):
        # create ptrs file with 20 days both in past and future
        back_forth = 20

        # create ptrs folder
        os.makedirs(os.path.dirname(self.ptr_folder_path))

        for i in range(-back_forth, back_forth):
            rel_index: str = str(Day.get_rel_index_dates_around_today(i))
            folder_path: str = self.ptr_folder_path + rel_index

            # create path with rel index and ptr file inside
            os.makedirs(folder_path)
            with open(folder_path + self.ptrs_file_name, 'w') as file:
                pass

    def get_user_info(self):
        with open(self.user_path, 'r') as file:
            user_data = json.load(file)
            self.lang = user_data['lang']
            self.is_euro_date = user_data['is_euro_date']
            self.name = user_data['name']

    def set_user_info(self):
        self.user_data = {
            "lang": self.lang,
            "is_euro_date": self.is_euro_date,
            "name": self.name
        }
        with open(self.user_path, 'w') as file:  # create user file
            json.dump(self.user_data, file, indent=4)

        # nice spacing
        Day.print_with_div(self.get_lang_spec_output(Output.welcome_new_o), self.name, char='*')
        print()

        self.user_edit_in_prog = False

    def is_user_info_changed(self) -> bool:
        if not (os.path.exists(self.user_path)):
            return True

        with open(self.user_path, 'r') as file:
            user_data = json.load(file)

            if user_data != self.user_data:
                return True

        return False

    def pos_handler(self, mod: int):
        # go back one (t)
        if mod == -1:
            self.update_cur_pos(self.cur_pos[:-1])
            return

        # go back to main menu (mm)
        elif mod == -2:
            if self.already_user:
                self.update_cur_pos(Output.all_pos_names_o['mm'])
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
        self.update_cur_pos(self.cur_pos + str(mod))

    # update cur_pos and prev_pos
    def update_cur_pos(self, new_pos: str):
        self.prev_pos = self.cur_pos
        self.cur_pos = new_pos

    # handle all user inputs based on prompts in output
    def input_handler(self, prompt: list[str | int], dyn_num_inputs: int):
        # set num_inputs/_type according to appendicies of prompt
        num_inputs_type = prompt[-1]
        num_inputs = prompt[-1]
        if num_inputs == 1:
            num_inputs = dyn_num_inputs
            num_inputs_type = -3  # change to auto next and save as cur_in
        elif num_inputs_type < 0:
            num_inputs = prompt[-2]

        while True:
            user_input: str = input(prompt[self.lang] + '\n')
            print()  # extra line below answer

            # remove empty spaces
            self.cur_in = ' '.join(user_input.split())

            # check always ops
            if self.check_always_op_and_update():
                return

            # hit enter for last op
            if self.cur_in == '':
                if num_inputs_type == -1:  # unless we need an actual answer
                    print(self.get_lang_spec_output(Output.no_empty_o))
                    continue
                elif num_inputs_type == 0:  # save cur_in and don't change position
                    self.prev_pos = self.cur_pos
                    return
                elif num_inputs_type == -3:  # auto next and save pos info in cur_in
                    self.auto_next_pos()
                    self.cur_in = str(num_inputs - 1)  # last option
                    return

                # handle empty input as last option
                self.pos_handler(num_inputs - 1)
                return

            # input = output
            elif num_inputs == 0:
                # pure in and out (only 0 appenedged to prompt) stays in same pos
                if num_inputs_type == 0:
                    self.prev_pos = self.cur_pos
                else:
                    self.auto_next_pos()
                return

            # all remaining ops have range check
            # check if type = -1 to auto next instead of move to actual option
            if self.is_valid_range(num_inputs):
                if num_inputs_type == -3:
                    self.auto_next_pos()
                else:
                    self.pos_handler(int(self.cur_in))
                return

            # out of range number and needs to be number
            elif self.cur_in.isdigit() and num_inputs_type != -2:
                print(self.get_lang_spec_output(Output.out_of_range_o))
                return

            # not a number and needs to be so invalid input
            if num_inputs_type != -2:
                print(self.get_lang_spec_output(Output.invalid_o))
                return

            # either in = out (specific pos) OR normal range check
            # and just checked range above so must be in = out
            else:
                self.pos_handler(0)  # in = out will be the 0th option
                return

    # only one prompt/level that could be next
    def auto_next_pos(self):
        self.update_cur_pos(self.cur_pos + '_')

    # check whether input is in range
    def is_valid_range(self, num_inputs: int) -> bool:
        if self.cur_in.isdigit():  # make sure its a number b4 forcing below
            return int(self.cur_in) < num_inputs
        return False

    # check always ops and move pos if need be
    def check_always_op_and_update(self) -> bool:
        for i in range(len(self.always_ops)):
            if self.cur_in == self.always_ops[i]:
                self.pos_handler(-i - 1)
                return True

        # not an always op
        return False

    # get output specific to user lange
    def get_lang_spec_output(self, output_all):
        return output_all[self.lang]
