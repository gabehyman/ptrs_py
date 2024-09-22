# import pyperclip # copy to clipboard

from user import User
from output import Output
from sort import Sort

# create objects
userer: User = User()

# get user info or make it if not there
userer.user_info()

# sort pointers
sorter: Sort = Sort(userer.ptrs_path)

cur_pos = '_'  # starting position
cur_out = ''  # starting output
day = 0
while True:
    show_day = True  # will show day if not modified

    # end program
    if cur_pos == '':
        userer.just_print(Output.afscheid_o, userer.name, True)
        break

    # _2 and _ are the same so just handle it in _
    elif cur_pos == '_2':
        cur_pos = '_'
    # show random day
    if cur_pos == '_':
        day = sorter.get_rand_day()
        if day == -1:
            userer.just_print(Output.empty_comp_o)
            show_day = False

    # enter write and show last day
    elif cur_pos == '_0':
        day = sorter.get_last_day()
    # search
    elif cur_pos == '_1':
        # just prompt search if no output (i.e first round)
        if not cur_out:
            show_day = False

        # process search with output
        else:
            search_params = sorter.determine_search(cur_out)
            if len(search_params) < 4:
                addendum = userer.search_error_addendum(search_params)

                userer.just_print(Output.invalid_search_o, addendum)
                show_day = False
            else:
                show_day = True

    elif cur_pos == '_00':
        # enter edit
        show_day = False
    elif cur_pos == '_01':
        # show next day
        day = sorter.next_day(day)
        cur_pos = userer.pos_handler(cur_pos, '-1')
    elif cur_pos == '_02':
        # show prev day
        day = sorter.prev_day(day)
        cur_pos = userer.pos_handler(cur_pos, '-1')

    # control to show day or not
    if show_day:
        sorter.days[day].print_all_ptrs(userer.lang)  # show day
    output = userer.input_handler(Output.all_pos_o[userer.repeat_prompt(cur_pos)], cur_pos)
    cur_pos = output[0]  # save positional info input
    cur_out = output[1]  # save user output info
