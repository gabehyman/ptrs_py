class Output:
    # outputs
    divider_o: str = '---------------------------------------'
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
                          'agrega algunos ptrs para ver un dia aleatario'
                          'voeg wat ptrs toe om een willekeurige dag te zien']
    no_empty_o: list[str] = ['i need an answer', 'necesito respuesta', 'ik heb een antwoord nodig']
    invalid_o: list[str] = ['invalid input. type the # that corresponds with what you wanna do',
                            'entrada invalida. pon el numero que corresponde con lo que quieres hacer',
                            'ongeldige invoer. geef het nummer die past met wat je wil doen']

    # prompts
    # _o[-1] = num options OR if = 0 then there needs to be a response
    # if _o[-1] = 0, then _o[-2] = num options to check range of answer
    # if _o[-2] = -1, then any answer is accepted
    language_o: list[str] = ['0 = english | 1 = espanol | 2 = nederlands.', '3', '0']
    name_o: list[str] = ['what\'s your name?', '¿como se llama?', 'hoe heet u?', '-1', '0']
    looking_at_day_o: list[str] = ['type to add new ptr(s) |\n0 = edit | 1 = previous day | 2 = next day.',
                                   'escribe para agregar un(os) ptr(s) nuevo |\n0 = editar | 1 = dia anterior | 2 = dia siguente.',
                                   'type om een nieuwe ptr(s) toe te voegen |\n0 = wijzigen | 1 = vorige dag | 2 = volgende dag.',
                                   '3', '-1']

    pos_o_: list[str] = ['0 = write | 1 = search | 2 = another random day.',
                         '0 = escribir | 1 = buscar | 2 = otro dia aleatario.',
                         '0 = schrijven | 1 = zoeken | 2 = andere willekeurige dag.',
                         '3']
    pos_o_1: list[str] = ['0 = by date | 1 = by word.',
                          '0 = por fecha | 1 = por palabra.',
                          '0 = per dag | 1 = per woord.',
                          '2']
    pos_o_10: list[str] = ['type date (12abc34 - 56def78) |\n0 = random.',
                           'entra fecha (12abc34 - 56def78) |\n0 = aleatoria.',
                           'geef datum (12abc34 - 56def78) |\n0 = willkeurige.',
                           '1', '-1']
    pos_o_11: list[str] = ['0 = continuous | 1 = exact | 2 = all | 3 = any',
                           '0 = continuo | 1 = exacto | 2 = todas | 3 = cualquier',
                           '0 = continu | 1 = precies | 2 = allen | 3 = elke',
                           '4']

    all_pos_o: dict[str, list[str]] = {
        '_': pos_o_,
        '_0': looking_at_day_o,
        '_1': pos_o_1,
        '_10': pos_o_10,
        '_11': pos_o_11}

