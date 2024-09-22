class Output:
    # outputs
    divider_o: str = '---------------------------------------'
    welcome_new_o: list[str] = ['welcome, ',
                                'bienvenido, ',
                                'welkom, ']
    welcome_o: list[str] = ['welcome back, ',
                            'bienvenido de vuelta, ',
                            'welkom terug, ']
    afscheid_o: list[str] = ['peace, ',
                             'ciao, ',
                             'later, ']
    empty_o: list[str] = ['<no ptrs on this day>',
                          '<no ptrs en este dia>'
                          '<geen ptrs op deze dag>']
    empty_comp_o: list[str] = ['add ptrs to be shown a random day',
                               'agrega algunos ptrs para ver un dia aleatario',
                               'voeg wat ptrs toe om een willekeurige dag te zien']
    no_empty_o: list[str] = ['i need an answer', 'necesito respuesta', 'ik heb een antwoord nodig']
    invalid_o: list[str] = ['invalid input. type the # that corresponds with what you wanna do',
                            'entrada invalida. pon el numero que corresponde con lo que quieres hacer',
                            'ongeldige invoer. geef het nummer die past met wat je wil doen']
    invalid_search_o: list[str] = ['invalid search due to the following: ',
                                   'busqueda invalida debido a lo siguente: ',
                                   'ongeldige opzoek vanwege het volgende: ']
    syntax_error_o: list[str] = ['syntax error in ',
                                 'error sintactico en ',
                                 'syntaxisfout in ']
    date_error_o: list[str] = ['invalid date',
                               'fecha invalida',
                               'ongeldige datum']
    date_range_error_o: list[str] = ['date outside range of your ptrs',
                                     'fecha fuera del rango de su ptrs',
                                     'datum buiten bereik van uw ptrs']

    # prompts
    # _o[-1] = num options OR if = 0 then there needs to be a response
    # _o[-1] = -1 -> can just write ptrs but can also pick option
    # if _o[-1] = 0 -> then _o[-2] = num options to check range of answer
    # if _o[-2] = -1 -> response in = response out (dont check always ops available)
    # if _o[-2] = -2 -> response in = response out (check always ops always ops available)
    language_o: list[str] = ['0 = english | 1 = espanol | 2 = nederlands.', '3', '0']
    name_o: list[str] = ['what\'s your name?', '¿como se llama?', 'hoe heet u?', '-1', '0']
    looking_at_day_o: list[str] = ['type to add new ptr(s) |\n0 = edit | 1 = previous day | 2 = next day.',
                                   'escribe para agregar un(os) ptr(s) nuevo |\n0 = editar | 1 = dia anterior | 2 = dia siguente.',
                                   'type om een nieuwe ptr(s) toe te voegen |\n0 = wijzigen | 1 = vorige dag | 2 = volgende dag.',
                                   '3', '-1']

    main_menu_o: list[str] = ['0 = write | 1 = search | 2 = another random day.',
                              '0 = escribir | 1 = buscar | 2 = otro dia aleatario.',
                              '0 = schrijven | 1 = zoeken | 2 = andere willekeurige dag.',
                              '3']
    prompt_search_o: list[str] = ['type what you want to search.',
                                  'entra lo que quiere buscar.',
                                  'geef wat u wilt zoeken.',
                                  '-2', '0']

    all_pos_o: dict[str, list[str]] = {
        '_': main_menu_o,
        '_0': looking_at_day_o,
        '_1': prompt_search_o}

    # same_prompt: list[str] = ['_11']
