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

cur_pos = '_'  # starting positions
day = 0
while True:
    show_day = True  # will show day if not modified

    if cur_pos == '':  # end program
        userer.just_print(Output.afscheid_o, True, True)
        break

    # _2 and _ are the same so just handle it in _
    elif cur_pos == '_2':
        cur_pos = '_'
    if cur_pos == '_':
        day = sorter.get_rand_day()
        if day == -1:
            userer.just_print(Output.empty_comp_o)
            show_day = False

    elif cur_pos == '_0':
        day = sorter.get_last_day()
    # elif cur_pos == '_1': just printing
        # enter search
    # elif cur_pos == '_2': not needed as we handle with '_'

    # elif cur_pos == '_00': just printing
        # enter edit
    elif cur_pos == '_01':
        day = sorter.next_day(day)
        cur_pos = userer.pos_handler(cur_pos, '-1')
    elif cur_pos == '_02':
        day = sorter.prev_day(day)
        cur_pos = userer.pos_handler(cur_pos, '-1')

    # control to show day or not
    if show_day:
        sorter.days[day].print_all_ptrs(userer.lang)  # show day
    cur_pos = userer.input_handler(Output.all_pos_o[cur_pos], cur_pos)  # take input
