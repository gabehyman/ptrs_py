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

    if cur_pos == '':
        # end program
        userer.just_print(Output.afscheid_o, True, True)
        break

    elif cur_pos == '_2':
        # _2 and _ are the same so just handle it in _
        cur_pos = '_'
    if cur_pos == '_':
        # show random day
        day = sorter.get_rand_day()
        if day == -1:
            userer.just_print(Output.empty_comp_o)
            show_day = False

    elif cur_pos == '_0':
        # enter write and show last day
        day = sorter.get_last_day()
    elif cur_pos == '_1':
        # search
        # prompt search if no output
        if not cur_out:
            show_day = False
        # conduct search with output
        else:
            sorter.determine_search(cur_out)
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
