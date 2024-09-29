# import pyperclip # copy to clipboard

from user import User
from output import Output
from sort import Sort
from search import Search

# print line for nice spacing at start
print()

# create user and create ptrs file if necessary
userer: User = User()

# create sorter
sorter: Sort = Sort(userer.ptrs_path)

lang_prev = -1  # store prev lang temp in case not changed
day = 0  # which day to show
while userer.cur_pos != '':  # end porgram
    show_day = False  # will not show day by default

    # ----- userer.cur_pos -> tracks user in program ----- #

    # get user lang
    if userer.cur_pos == '_':
        lang_prev = userer.lang
        userer.lang = 0  # reset lang (only one element in lang output array)
        userer.user_edit_in_prog = True  # user info is being updated
        userer.just_print(Output.divider_o)

    # get user name
    elif userer.cur_pos == '__':
        # only update if user editting already in progress (ie coming from '_')
        if userer.user_edit_in_prog:
            userer.lang = int(userer.cur_out)
            lang_prev = -1
        else:
            userer.just_print(Output.divider_o)

            # so we know to update file if just editing name (did not go back to lang)
            userer.user_edit_in_prog = True  # user info is being updated

    # _2 and _ are the same so just handle it in _
    elif userer.cur_pos == '___2':
        userer.pos_handler(-1)
    # show main menu with random day
    if userer.cur_pos == '___':
        # write user info to file if needs updating
        if userer.user_edit_in_prog:
            # if last in was always op, don't update name
            if userer.cur_in not in userer.always_ops:
                # last input given must be name
                userer.name = userer.cur_out
                userer.already_user = True
            else:
                if lang_prev != -1:
                    userer.lang = lang_prev
                    lang_prev = -1

            if userer.is_user_info_changed():
                userer.update_user()

            userer.user_edit_in_prog = False

        day = sorter.get_rand_day()
        if day == -1:  # all pointers empty
            userer.just_print(userer.get_lang_spec_output(Output.all_days_empty_o))
            show_day = False

    # enter write and show last day
    elif userer.cur_pos == '___0':
        day = sorter.get_last_day()
    # prompt search
    # elif userer.cur_pos == '___1':
        # just prompts search so don't need to do anything

    elif userer.cur_pos == '___00':
        # enter edit
        show_day = False
    elif userer.cur_pos == '___01':
        # show next day
        day = sorter.next_day(day)
        userer.pos_handler(-1)
    elif userer.cur_pos == '___02':
        # show prev day
        day = sorter.prev_day(day)
        userer.pos_handler(-1)

    elif userer.cur_pos == '___1_':
        # create searcher (which has a reference to sorter)
        searcher: Search = Search(sorter)

        # parse search
        searcher.parse_search(userer.cur_pos)
        if searcher.is_valid_search:
            print('nice')
        else:
            userer.pos_handler(-1)
            userer.just_print(searcher.get_search_error_output())

        show_day = False

    # control to show day or not
    if show_day:
        sorter.days[day].print_all_ptrs(userer.lang)  # show day

    userer.input_handler(Output.all_pos_o[userer.cur_pos])

userer.just_print(userer.get_lang_spec_output(Output.afscheid_o), True)  # ptrs closed, neem afscheid

