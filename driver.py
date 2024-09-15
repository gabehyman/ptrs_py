# import pyperclip # copy to clipboard
import random as rand

from user import User
from output import Output
from sort import Sort

# create objects
userer: User = User()

# get user info or make it if not there
print(f'\n{Output.divider_o}')
userer.user_info()
userer.just_print_i(Output.welcome_o, 1)
print(f'{Output.divider_o}\n')

# sort pointers
sorter: Sort = Sort(userer.ptrs_path)

cur_pos = '_'  # starting positions
day = 0
while True:
    if cur_pos == '':  # end program
        userer.just_print_i(Output.afscheid_o, 1)
        break
    # _2 and _ are the same so just handle it in _
    elif cur_pos == '_2':
        cur_pos = '_'
    if cur_pos == '_':
        # no ptrs have been written
        if sorter.has_ptrs:
            # don't show days with no ptrs written
            while True:
                day = rand.randint(0, len(sorter.days))  # rando day
                if sorter.days[day].has_ptrs():
                    break
                else:
                    continue

            sorter.days[day].print_all_ptrs(userer.lang)  # show day

        else:
            userer.just_print_i(Output.empty_comp_o)

    elif cur_pos == '_0':
        day = len(sorter.days) - 1

        sorter.days[day].print_all_ptrs(userer.lang)  # show day
    elif cur_pos == '_1':
        # enter search
        day
    # dont need '_2' as it just stays '_'

    elif cur_pos == '_00':
        # enter edit
        day
    elif cur_pos == '_01':
        day += (day + 1) % len(sorter.days)
        cur_pos = userer.pos_handler(cur_pos, '-1')

        sorter.days[day].print_all_ptrs(userer.lang)  # show day
    elif cur_pos == '_02':
        day += (day - 1 + len(sorter.days)) % len(sorter.days)
        cur_pos = userer.pos_handler(cur_pos, '-1')

        sorter.days[day].print_all_ptrs(userer.lang)  # show day

    cur_pos = userer.input_handler(Output.all_pos_o[cur_pos], cur_pos)  # take input
