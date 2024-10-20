# import pyperclip # copy to clipboard

from user import User
from output import Output
from sort import Sort
from search import Search
from day import Day

# nice spacing at start
print()

# create user and create ptrs file if necessary
userer: User = User()

# create sorter
sorter: Sort = Sort(userer.ptrs_path, userer.is_euro_date)

# declare searcher (new searcher for every new search)
searcher: Search

day = 0  # which day to show
dyn_range_inputs = 0  # store a dynamic range of inputs (eg #days with finds)
while userer.cur_pos != '':  # end porgram
    show_day = False  # will not show day by default

    # ----- userer.cur_pos -> tracks user in program ----- #
    # ----- userer.cur_in -> stores users last input ----- #

    # get user lang
    if userer.cur_pos == Output.all_pos_names_o['lang']:
        userer.user_edit_in_prog = True  # user info is being updated
        print(Output.divider_o)

    # get user name
    elif userer.cur_pos == Output.all_pos_names_o['name']:
        # only update if user editting already in progress (ie coming from '_')
        if userer.user_edit_in_prog:
            userer.lang = int(userer.cur_in)
        else:
            print(Output.divider_o)

            # so we know to update file if just editing name (did not go back to lang)
            userer.user_edit_in_prog = True  # user info is being updated

    # show main menu with random day
    if userer.cur_pos == Output.all_pos_names_o['mm']:
        if userer.has_searched:  # go back to search results
            userer.cur_pos = Output.all_pos_names_o['show_search']
        else:
            # write user info to file if needs updating
            if userer.user_edit_in_prog:
                # check if last in was mm, so we know not to update name
                if userer.cur_in != User.always_ops[1]:
                    # otherwise last input given must be name
                    userer.name = userer.cur_in
                    userer.already_user = True

                # compares with file values
                if userer.is_user_info_changed():
                    userer.update_user()

                userer.user_edit_in_prog = False

            day = sorter.get_rand_day()
            if day == -1:  # all pointers empty
                print(userer.get_lang_spec_output(Output.all_days_empty_o))
            else:
                show_day = True

    # enter look at day and show last day
    # if and not elif so that if we have go back to mm with a search it will show search
    if userer.cur_pos == Output.all_pos_names_o['lad']:
        day = sorter.get_last_day()
        show_day = True

    # prompt search
    elif userer.cur_pos == Output.all_pos_names_o['prompt_search']:
        userer.has_searched = False  # reset so we create a new searcher

    elif userer.cur_pos == Output.all_pos_names_o['go_to_day']:
        if day == -1:  # all pointers empty
            print(userer.get_lang_spec_output(Output.all_days_empty_o))
            # go back to main menu
            userer.pos_handler(-2)
        else:
            # enter look at day with shown day (don't show)
            userer.cur_pos = Output.all_pos_names_o['lad']

    # ___3 and ___ are the same so just handle it in ___
    elif userer.cur_pos == Output.all_pos_names_o['rand_day']:
        # go back to main menu
        userer.pos_handler(-2)

    # enter edit
    # elif userer.cur_pos == Output.all_pos_names_o['edit']:
    # just prompt edit options (don't show)

    # show prev day
    elif userer.cur_pos == Output.all_pos_names_o['prev_day']:
        day = sorter.prev_day(day)
        userer.pos_handler(-1)
        show_day = True

    # show next day
    elif userer.cur_pos == Output.all_pos_names_o['next_day']:
        day = sorter.next_day(day)
        userer.pos_handler(-1)
        show_day = True

    # enter search
    if userer.cur_pos == Output.all_pos_names_o['show_search']:
        # only create new searcher if not coming back from a picked searched day
        if not userer.has_searched:
            # create searcher (which has a reference to sorter)
            searcher = Search(sorter)

            # parse user input
            searcher.parse_search(userer.cur_in)
            if searcher.is_valid_search:
                searcher.do_search()

            else:  # invalid search
                userer.pos_handler(-1)
                print((userer.get_lang_spec_output(searcher.get_search_error_output())
                       + f' (keyword = {searcher.keyword_error})'))

        if searcher.finds_day_is:  # if we have finds
            for i in range(searcher.num_days_find):
                # search each day in finds and print
                day_search = sorter.days[sorter.rel_index_to_user_days(searcher.finds_day_is[i])]
                day_search.print_search_ptrs(userer.lang, i, searcher.finds_is[i], searcher.search_clauses,
                                             searcher.context)

            # update allowed range of input based on #days with finds
            dyn_range_inputs = searcher.num_days_find
            userer.has_searched = True  # mark that we've searched

        else:  # no finds
            userer.pos_handler(-1)
            print(userer.get_lang_spec_output(Output.no_finds_o))

    # pick a day with a find to go into (prompt = lad but distinct so they can go back to search)
    elif userer.cur_pos == Output.all_pos_names_o['pick_day']:
        # enter look at day with desired search day
        userer.cur_pos = Output.all_pos_names_o['lad']
        day = sorter.rel_index_to_user_days(searcher.finds_day_is[(int(userer.cur_in))])
        show_day = True

    if show_day:  # control to show day or not
        sorter.days[day].print_all_ptrs(userer.lang)

    # handle user input and determine next position in program
    userer.input_handler(Output.all_pos_o[userer.cur_pos], dyn_range_inputs)

# ptrs closed, neem afscheid
Day.print_with_div(userer.get_lang_spec_output(Output.afscheid_o), userer.name, char='#')
