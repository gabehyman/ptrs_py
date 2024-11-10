import os
from datetime import datetime

months: list[list[str]] = [
        ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
         'december'],
        ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
         'deciembre'],
        ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november',
         'december']]
start_of_time: datetime = datetime(1999, 8, 24)


def ptrs_file_to_folder(ptrs_file_path: str, ptr_folders_path: str, numbered_date: bool = False):
    # make ptrs folder
    os.makedirs(ptr_folders_path)
    with open(ptrs_file_path, 'r') as file:
        for line in file:
            line_ind = line.split()

            if not numbered_date:
                # get parts of date
                day = line_ind[0]
                line_ind.pop(0)

                month_s = line_ind[0]
                line_ind.pop(0)
                month = 0
                for i in range(len(months[2])):
                    if month_s[:-1] == months[2][i]:
                        month = i + 1
                        break

                year = line_ind[0]
                line_ind.pop(0)
                line_ind.pop(0)
            else:
                date = line_ind[0].split('/')
                line_ind.pop(0)
                line_ind.pop(0)

                day = date[0]
                month = date[1]
                year = date[2]

            date_obj: datetime = datetime(int(year), int(month), int(day))
            rel_index = (date_obj - start_of_time).days

            day_path: str = ptr_folders_path + str(rel_index)
            os.makedirs(day_path)

            print()
            print(f'writing {day} {months[2][month-1]}, {year}...')

            with open(day_path + '/ptrs.txt', 'w') as file_small:
                file_small.write(' '.join(line_ind) + '\n')


wd: str = '/Users/gabehyman/PycharmProjects/ptrs_py'
ptrs_file_to_folder('/Users/gabehyman/Desktop/pters.txt', f'{wd}/ptrs/')

