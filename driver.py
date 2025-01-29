from user import User
from output import Output
from sort import Sort
from search import Search
from day import Day
import pyperclip

# nice spacing at start
print()

# create user and create ptrs file if necessary
userer: User = User()

# create sorter
sorter: Sort = Sort(userer)

# declare searcher (new searcher for every new search)
searcher: Search

day = 0  # which day to show
dyn_range_inputs = 0  # store a dynamic range of inputs (eg #days with finds)
while userer.cur_pos != '':  # end program
    show_day = False  # will not show day by default

    # ----- userer.cur_pos -> tracks user in program ----- #
    # ----- userer.cur_in -> stores users last input ----- #

    # get user lang
    if userer.cur_pos == Output.all_pos_names_o['lang']:
        userer.user_edit_in_prog = True  # user info is being updated
        print(Output.divider_o)

    # get user date preference
    elif userer.cur_pos == Output.all_pos_names_o['date']:
        # nothing to update if coming back from name
        if userer.cur_in != User.always_ops[0]:
            userer.lang = int(userer.cur_in)

    # get user name
    elif userer.cur_pos == Output.all_pos_names_o['name']:
        # only update if user editting already in progress (ie coming from '_')
        if userer.user_edit_in_prog:
            userer.is_euro_date = bool(int(userer.cur_in))
        else:
            print(Output.divider_o)

            # so we know to update file if just editing name (did not go back to lang)
            userer.user_edit_in_prog = True  # user info is being updated

    # show another rand day (revert to main menu)
    if userer.cur_pos == Output.all_pos_names_o['rand_day']:
        userer.update_cur_pos(Output.all_pos_names_o['mm'])
    # show main menu with random day
    if userer.cur_pos == Output.all_pos_names_o['mm']:
        if userer.has_searched:  # go back to search results
            # if only one day found go back to search results
            if len(searcher.finds_day_is) == 1:
                userer.update_cur_pos(Output.all_pos_names_o['prompt_search'])
            # otherwise display all results again
            else:
                userer.update_cur_pos(Output.all_pos_names_o['show_search'])
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
                    userer.set_user_info()

                userer.user_edit_in_prog = False

            day = sorter.get_rand_day()
            if day == -1:  # all pointers empty
                print(userer.get_lang_spec_output(Output.all_days_empty_o))
            else:
                show_day = True

    # enter look at day and show last day
    # if and not elif so that if we have go back to mm with a search it will show search
    if userer.cur_pos == Output.all_pos_names_o['lad']:
        # user chooses to start writing from mm, so show them last day
        if userer.prev_pos == Output.all_pos_names_o['mm']:
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
            userer.update_cur_pos(Output.all_pos_names_o['lad'])
            show_day = True

    # ___3 and ___ are the same so just handle it in ___
    elif userer.cur_pos == Output.all_pos_names_o['rand_day']:
        # go back to main menu
        userer.pos_handler(-2)

    # enter edit
    elif userer.cur_pos == Output.all_pos_names_o['edit']:
        # if we were previously editing OR cur_in != last value of ['edit'] == '0'
        # (actually giving a ptr to write not a 0 coming from lad), we write
        if (userer.prev_pos == Output.all_pos_names_o['edit'] or
                userer.cur_in != Output.all_pos_names_o['edit'][-1]):
            # go to write (but don't change prev_pos so we can check in write if we append or not)
            userer.cur_pos = Output.all_pos_names_o['write']

        # copy csv ptrs to clipboard to make editing easy
        elif sorter.days[day].has_ptrs():
            pyperclip.copy(sorter.days[day].get_all_ptrs_csv())

    # handles writing (has to come from edit and will always go back to edit)
    if userer.cur_pos == Output.all_pos_names_o['write']:
        sorter.days[day].write_ptrs(userer.cur_in, userer.ptr_folder_path, userer.ptrs_file_name,
                                    userer.prev_pos == Output.all_pos_names_o['lad'])  # append if from lad
        userer.update_cur_pos(Output.all_pos_names_o['edit'])
        show_day = True

    # show prev day
    elif userer.cur_pos == Output.all_pos_names_o['prev_day']:
        day -= 1  # decrement day
        if day < 0:  # ask if user wants to wrap to end or create new day
            userer.input_handler(Output.new_day_or_wrap_o, dyn_range_inputs)
        else:  # not an edge case so day is correctly updated and go back to lad
            userer.update_cur_pos(Output.all_pos_names_o['lad'])
            show_day = True

    # show next day
    elif userer.cur_pos == Output.all_pos_names_o['next_day']:
        day += 1  # increase day
        if day >= len(sorter.days):  # ask if user wants to wrap to start or create new day
            userer.input_handler(Output.new_day_or_wrap_o, dyn_range_inputs)
        else:  # not an edge case so day is correctly updated and go back to lad
            userer.update_cur_pos(Output.all_pos_names_o['lad'])
            show_day = True

    # creates new prev day
    if userer.cur_pos == Output.all_pos_names_o['new_prev']:
        sorter.make_new_days(day, True, userer.ptr_folder_path, userer.ptrs_file_name)
        userer.update_cur_pos(Output.all_pos_names_o['lad'])
        day = 0
        show_day = True

    # creates new next day
    elif userer.cur_pos == Output.all_pos_names_o['new_next']:
        sorter.make_new_days(day, False, userer.ptr_folder_path, userer.ptrs_file_name)
        userer.update_cur_pos(Output.all_pos_names_o['lad'])
        show_day = True

    # wraps around to start of list of days
    elif userer.cur_pos == Output.all_pos_names_o['wrap_next']:
        day = sorter.next_day(day)
        userer.update_cur_pos(Output.all_pos_names_o['lad'])
        show_day = True

    # wraps around to end of list of days
    elif userer.cur_pos == Output.all_pos_names_o['wrap_prev']:
        day = sorter.prev_day(day)
        userer.update_cur_pos(Output.all_pos_names_o['lad'])
        show_day = True

    # enter search
    if userer.cur_pos == Output.all_pos_names_o['show_search']:
        # only create new searcher if not coming back from a picked searched day
        if not userer.has_searched:
            # create searcher (which has a reference to sorter)
            searcher = Search(sorter)

            # parse user input
            searcher.parse_search(userer.cur_in)
            if not searcher.is_valid_search:
                userer.pos_handler(-1)
                print((userer.get_lang_spec_output(searcher.get_search_error_output())
                       + f' (keyword = {searcher.keyword_error})'))

            else:
                searcher.do_search()

        # if we have finds (if invalid search, no finds)
        if searcher.finds_day_is:
            if len(searcher.finds_day_is) == 1:
                # pass in num_day = -1 when only one day found
                day = sorter.rel_index_to_user_days(searcher.finds_day_is[0])
                day_search = sorter.days[day]

                # only show valid finds for the day
                search_clauses = searcher.search_clauses
                if search_clauses and searcher.finds_actual_clauses[0]:
                    search_clauses = [searcher.search_clauses[i] for i in searcher.finds_actual_clauses[0]]
                day_search.print_search_ptrs(userer.lang, -1, searcher.finds_is[0], search_clauses,
                                             searcher.context, userer.is_euro_date)

                # automatically go to looking at that particular day
                userer.update_cur_pos(Output.all_pos_names_o['lad'])
            else:
                for i in range(searcher.num_days_find):
                    # search each day in finds and print
                    day_search = sorter.days[sorter.rel_index_to_user_days(searcher.finds_day_is[i])]

                    # only show valid finds for the day
                    search_clauses = searcher.search_clauses
                    if searcher.finds_actual_clauses[0]:
                        search_clauses = [searcher.search_clauses[i] for i in searcher.finds_actual_clauses[0]]
                    day_search.print_search_ptrs(userer.lang, i, searcher.finds_is[i], search_clauses,
                                                 searcher.context, userer.is_euro_date)

            # update allowed range of input based on #days with finds
            dyn_range_inputs = searcher.num_days_find
            userer.has_searched = True  # mark that we've searched

        elif searcher.is_valid_search:  # valid search with no finds
            userer.pos_handler(-1)
            print(userer.get_lang_spec_output(Output.no_finds_o))

    # pick a day with a find to go into (prompt = lad but distinct so they can go back to search)
    elif userer.cur_pos == Output.all_pos_names_o['pick_day']:
        # enter look at day with desired search day
        userer.update_cur_pos(Output.all_pos_names_o['lad'])
        day = sorter.rel_index_to_user_days(searcher.finds_day_is[(int(userer.cur_in))])
        show_day = True

    if show_day:  # control to show day or not
        day_o = sorter.days[day]
        # if we just searched and the day we want to show was found, show the finds with -->
        if userer.has_searched and day_o.rel_index in searcher.finds_day_is:
            day_o.print_search_ptrs(userer.lang, -1, searcher.finds_is[searcher.finds_day_is.index(day_o.rel_index)],
                                    searcher.search_clauses, searcher.context, userer.is_euro_date)
        else:
            day_o.print_all_ptrs(userer.lang, userer.is_euro_date)

    # handle user input and determine next position in program
    userer.input_handler(Output.all_pos_o[userer.cur_pos], dyn_range_inputs)

# ptrs closed, neem afscheid
Day.print_with_div(userer.get_lang_spec_output(Output.afscheid_o), userer.name, char='#')
