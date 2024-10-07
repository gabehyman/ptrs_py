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
                          '<no ptrs en este dia>'
                          '<geen ptrs op deze dag>']
    all_days_empty_o: list[str] = ['add ptrs to be shown a random day.',
                                   'agrega algunos ptrs para ver un dia aleatario.',
                                   'voeg wat ptrs toe om een willekeurige dag te zien.']
    no_empty_o: list[str] = ['i need an answer.', 'necesito respuesta.', 'ik heb een antwoord nodig.']
    no_finds_o: list[str] = ['no matches.', 'no resultados.', 'geen resultaten.']
    invalid_o: list[str] = ['input out of range.',
                            'entrada fuera del rango.',
                            'invoer buiten bereik.']
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

    # prompts
    # _o[-1] = num options (i.e., check range) OR
    # _o[-1] = 1 -> num options is dynamic (eg #days with finds)
    # _o[-1] = 0 -> input = output (auto next, can't be empty)
    # _o[-1] = -1 -> check range BUT auto next and save pos info as cur_in
    # _o[-1] = -2 -> either in = out (specific pos) OR normal range check
    # if _o[-1] < 0 -> _o[-2] = num options
    language_o: list[str | int] = ['0 = english | 1 = spanish | 2 = dutch.',
                                   '0 = ingles | 1 = espanol | 2 = holandes.',
                                   '0 = engels | 1 = spaans | 2 = nederlands.',
                                   3, -1]
    name_o: list[str | int] = ['what\'s your name?',
                               '¿como se llama?',
                               'hoe heet u?',
                               0]
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
                                        0]
    show_search_o: list[str | int] = ['type the number that corresponds to the day you want to see in full.',
                                      'entra el numero del dia que quieres ver completo.',
                                      'geef het nummer van de dag die je volledig wil zien.',
                                      1]

    # map positions to outputs
    all_pos_o: dict[str, list[str]] = {
        '_': language_o,
        '__': name_o,
        '___': main_menu_o,
        '___0': looking_at_day_o,
        '___1': prompt_search_o,
        '___1_': show_search_o,
        '___1__': looking_at_day_o}

    # map general names of positions to positions
    all_pos_names_o: dict[str, str] = {
        'lang': '_',
        'name': '__',
        'mm': '___',
        'lad': '___0',
        'prompt_search': '___1',
        'go_to_day': '___2',
        'rand_day': '___3',
        'edit': '___00',
        'prev_day': '___01',
        'next_day': '___02',
        'show_search': '___1_',
        'pick_day': '___1__'}
