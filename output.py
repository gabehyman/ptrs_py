class Output:
    # outputs
    divider_o: str = '|-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-|'
    welcome_new_o: list[str] = ['welcome',
                                'bienvenido',
                                'welkom']
    welcome_o: list[str] = ['welcome back',
                            'bienvenido de vuelta',
                            'welkom terug']
    afscheid_o: list[str] = ['peace',
                             'ciao',
                             'later']
    mm_unavailable_o: list[str] = ['mm becomes available after inputting language and name preferences.',
                                   'mm estara disponible despues de entrar su preferencia de lengua y nombre.',
                                   'mm wordt beschikbaar nadat u uw taal en naam voorkeur geeft.']
    empty_o: list[str] = ['<no ptrs on this day>',
                          '<no ptrs en este dia>',
                          '<geen ptrs op deze dag>']
    all_days_empty_o: list[str] = ['add ptrs to be shown a random day.',
                                   'agrega algunos ptrs para ver un dia aleatario.',
                                   'voeg wat ptrs toe om een willekeurige dag te zien.']
    no_empty_o: list[str] = ['answer cannot be empty.', 'la respuesta no puede ser vacia.',
                             'het antwoord mag niet leeg zijn.']
    no_finds_o: list[str] = ['no matches.', 'no resultados.', 'geen resultaten.']
    out_of_range_o: list[str] = ['input out of range.',
                                 'entrada fuera del rango.',
                                 'invoer buiten bereik.']
    invalid_o: list[str] = ['invalid input.',
                            'entrada invalida.',
                            'ongeldige invoer.']
    invalid_search_o: list[str] = ['invalid search due to the following: ',
                                   'busqueda invalida debido a lo siguente: ',
                                   'ongeldige opzoek vanwege het volgende: ']
    syntax_error_o: list[str] = ['syntax error',
                                 'error sintactico',
                                 'syntaxisfout']
    keyword_error_o: list[str] = ['invalid keyword input',
                                  'entrada de keyword invalida',
                                  'ongeldige keyword invoer']
    date_range_error_o: list[str] = ['date outside of range error',
                                     'error de fecha fuera del rango',
                                     'datum buiten bereik fout']

    # num_inputs_type = prompt[-1]
    # num_inputs = prompt[-1]
    # if num_inputs == 1:
    #     num_inputs = dyn_num_inputs
    # elif num_inputs_type < 0:
    #     num_inputs = prompt[-2]
    # ^^ input handler code ^^

    # _o[-1] = 1 -> num options is dynamic (eg #days with finds)
    # _o[-2 or -1] = 0 -> input = output (auto next)
    #   # _o[-1] = -1 -> can't empty
    # _o[-2] = -2 ->  normal range check OR either in = out
    # _o[-2] = -3 -> check range BUT auto next and save pos info as cur_in
    language_o: list[str | int] = ['0 = english | 1 = spanish | 2 = dutch.',
                                   '0 = ingles | 1 = espanol | 2 = holandes.',
                                   '0 = engels | 1 = spaans | 2 = nederlands.',
                                   3, -3]
    date_type_o: list[str | int] = ['0 = american date (mm/dd/yy) | 1 = european date (dd/mm/yy).',
                                    '0 = fecha americana (mm/dd/aa) | 1 = fecha europea (dd/mm/aa).',
                                    '0 = amerikaanse datum (mm/dd/jj) | 1 = europeese datum (dd/mm/jj).',
                                    2, -3]
    name_o: list[str | int] = ['what\'s your name?',
                               '¿como se llama?',
                               'hoe heet u?',
                               0, -1]
    looking_at_day_o: list[str | int] = ['type to add new ptr(s) |\n0 = edit | 1 = previous day | 2 = next day.',
                                         'escribe para agregar un(os) ptr(s) nuevo(s) |\n0 = editar | 1 = dia '
                                         'anterior | 2 = dia siguente.',
                                         'type om een nieuwe ptr(s) toe te voegen |\n0 = wijzigen | 1 = vorige dag | '
                                         '2 = volgende dag.',
                                         3, -2]
    main_menu_o: list[str | int] = ['0 = write | 1 = search | 2 = go to this day | 3 = another random day.',
                                    '0 = escribir | 1 = buscar | 2 = a este dia | 3 = otro dia aleatario.',
                                    '0 = schrijven | 1 = zoeken | 2 = naar deze dag | 3 = andere willekeurige dag.',
                                    4]
    prompt_search_o: list[str | int] = ['type what you want to search.',
                                        'entra lo que quiere buscar.',
                                        'geef wat u wilt zoeken.',
                                        0, -1]
    show_search_o: list[str | int] = ['type the number that corresponds to the day you want to see in full.',
                                      'entra el numero del dia que quieres ver completo.',
                                      'geef het nummer van de dag die je volledig wil zien.',
                                      1]
    edit_o: list[str | int] = ['cmd + v to paste all ptrs of the day and edit as you please.',
                               'cmd + v para pegar todos los ptrs del dia en edita como quiera.',
                               'cmd + v om alle ptrs van de dag te plakken en wijzig als u wilt.',
                               0]
    new_day_or_wrap_o: list[str | int] = ['0 = create new day | 1 = wrap around.',
                                          '0 = crear un dia nuevo | 1 = dar una vuelta.',
                                          '0 = nieuwe dag maken | 1 = rondgaan.',
                                          2]

    # prefix of main menu
    mm_prefix: str = '____'

    # map general names of positions to positions as tree
    # _ = auto next only option
    # x = stopping point and always goes back
    all_pos_names_o: dict[str, str] = {
        'lang': mm_prefix[:-3],
        'date': mm_prefix[:-2],
        'name': mm_prefix[:-1],
        'mm': mm_prefix,
        'lad': f'{mm_prefix}0',
        'prompt_search': f'{mm_prefix}1',
        'go_to_day': f'{mm_prefix}2',
        'rand_day': f'{mm_prefix}3',
        'write': f'{mm_prefix}00x',
        'edit': f'{mm_prefix}00',
        'prev_day': f'{mm_prefix}01',
        'next_day': f'{mm_prefix}02',
        'new_prev': f'{mm_prefix}010',
        'new_next': f'{mm_prefix}020',
        'wrap_prev': f'{mm_prefix}011',
        'wrap_next': f'{mm_prefix}021',
        'show_search': f'{mm_prefix}1_',
        'pick_day': f'{mm_prefix}1__'}

    # map positions to outputs
    all_pos_o: dict[str, list[str]] = {
        all_pos_names_o['lang']: language_o,
        all_pos_names_o['date']: date_type_o,
        all_pos_names_o['name']: name_o,
        all_pos_names_o['mm']: main_menu_o,
        all_pos_names_o['lad']: looking_at_day_o,
        all_pos_names_o['prompt_search']: prompt_search_o,
        all_pos_names_o['edit']: edit_o,
        all_pos_names_o['show_search']: show_search_o,
        all_pos_names_o['pick_day']: looking_at_day_o}
