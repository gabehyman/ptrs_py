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
    no_empty_o: list[str] = ['i need an answer', 'necesito respuesta', 'ik heb een antwoord nodig.']
    invalid_o: list[str] = ['invalid input. type the # that corresponds with what you wanna do.',
                            'entrada invalida. pon el numero que corresponde con lo que quieres hacer.',
                            'ongeldige invoer. geef het nummer die past met wat je wil doen.']
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
    # _o[-1] = 0 -> input = output (auto next, can't be empty)
    # _o[-1] = -1 -> check range BUT auto next and save pos info as cur_out
    # _o[-1] = -2 -> either in = out (specific pos) OR normal range check
    # if _o[-1] < 0 -> _o[-2] = num options
    language_o: list[str | int] = ['0 = english | 1 = espanol | 2 = nederlands.',
                                   3, -1]
    name_o: list[str | int] = ['what\'s your name?',
                               '¿como se llama?',
                               'hoe heet u?',
                               0]
    looking_at_day_o: list[str | int] = ['type to add new ptr(s) |\n0 = edit | 1 = previous day | 2 = next day.',
                                         'escribe para agregar un(os) ptr(s) nuevo |\n0 = editar | 1 = dia anterior | '
                                         '2 = dia siguente.',
                                         'type om een nieuwe ptr(s) toe te voegen |\n0 = wijzigen | 1 = vorige dag | '
                                         '2 = volgende dag.',
                                         3, -2]
    main_menu_o: list[str | int] = ['0 = write | 1 = search | 2 = another random day.',
                                    '0 = escribir | 1 = buscar | 2 = otro dia aleatario.',
                                    '0 = schrijven | 1 = zoeken | 2 = andere willekeurige dag.',
                                    3]
    prompt_search_o: list[str | int] = ['type what you want to search.',
                                        'entra lo que quiere buscar.',
                                        'geef wat u wilt zoeken.',
                                        0]

    all_pos_o: dict[str, list[str]] = {
        '_': language_o,
        '__': name_o,
        '___': main_menu_o,
        '___0': looking_at_day_o,
        '___1': prompt_search_o}

    # same_prompt: list[str] = ['_11']
