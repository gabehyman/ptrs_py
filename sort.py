from day import Day
from user import User
import random as rand
import hashlib
import os


class Sort:

    def __init__(self, userer: User):
        self.is_euro_date: bool = userer.is_euro_date

        # get first rel index and num of days
        self.first_rel_index = 100000  # ~275 years to start as min

        # get num of days to preallocate array and start of days (not super necessary but scalable/efficient)
        num_days = 0
        list_of_dirs: list[str] = os.listdir(userer.ptr_folder_path)
        for day_index in os.listdir(userer.ptr_folder_path):
            if day_index == '.DS_Store':  # ignore mac os file
                list_of_dirs.remove(day_index)
                continue
            day_index_int = int(day_index)
            # get first_rel_index
            if day_index_int < self.first_rel_index:
                self.first_rel_index = day_index_int

            num_days += 1

        # create days and populate days list in proper order
        self.days: list[Day] = [None] * num_days
        for day_index in list_of_dirs:
            day_ptr_path = userer.ptr_folder_path + day_index + userer.ptrs_file_name
            with open(day_ptr_path, 'r') as file:
                day: Day = Day(file.readline().strip(), int(day_index))
                self.days[self.rel_index_to_user_days(day.rel_index)] = day

        self.last_rel_index = self.days[-1].rel_index

    # check if user has written any ptrs
    def has_ptrs(self):
        for day in self.days:
            if day.has_ptrs():
                return True
        return False

    # get best last day top show
    def get_last_day(self):
        if not self.has_ptrs():
            return len(self.days) - 1  # show last day if no ptrs written
        else:
            # get last day with ptrs
            for i in reversed(range(len(self.days))):
                if self.days[i].has_ptrs():
                    return i

    # get a random day with ptrs
    def get_rand_day(self):
        # ptrs have been written
        if self.has_ptrs():
            # don't show days with no ptrs written
            while True:
                day = rand.randrange(len(self.days))  # rando day
                if self.days[day].has_ptrs():
                    return day
                else:
                    continue
        else:
            return -1

    # return same day or wrap around
    def next_day(self, new_day: int):
        return new_day % len(self.days)

    # return same day or wrap around
    def prev_day(self, new_day: int):
        return (new_day + len(self.days)) % len(self.days)

    # create new days at start or end of list (can be multiple)
    def make_new_days(self, new_days: int, append_front: bool, ptr_folder_path: str, ptrs_file_name: str):
        rel_index = self.user_days_to_rel_index(new_days)

        # get list of new days to make
        if append_front:
            range_new_days = range(self.first_rel_index - 1, rel_index - 1, -1)
        else:
            range_new_days = range(self.last_rel_index + 1, rel_index + 1)

        # create files and update program data
        for new_day in range_new_days:
            day_folder_path = ptr_folder_path + str(new_day)
            os.makedirs(day_folder_path)
            with open(day_folder_path + ptrs_file_name, 'w') as file:
                pass

            if append_front:
                self.days.insert(0, Day('', new_day))
            else:
                self.days.append(Day('', new_day))

        # update first adn last rel indicies with new days
        if append_front:
            self.first_rel_index = self.days[0].rel_index
        else:
            self.last_rel_index = self.days[-1].rel_index

    # convert relative index into user index
    def rel_index_to_user_days(self, rel_index: int):
        return rel_index - self.first_rel_index

    # convert user index to relative index
    def user_days_to_rel_index(self, user_day: int):
        return user_day + self.first_rel_index

    def folder_to_ptrs_file(self, ptrs_file_path: str, lang: int):
        with open(ptrs_file_path, 'w') as file:
            for day in self.days:
                date_str: str = f'({day.days_of_week[lang][day.day_of_week]}) {day.day} {day.months[lang][day.month-1]}, {day.year} ::  \t'
                file.write(date_str + day.get_all_ptrs_csv() + '\n')

    @staticmethod
    def ptrs_file_to_folder(ptrs_file_path: str, ptrs_folders_path: str, months: list[list[str]], lang:int, is_euro_date: bool):
        # make ptrs folder
        os.makedirs(ptrs_folders_path)
        with open(ptrs_file_path, 'r') as file:
            for line in file:
                line_ind = line.split()

                # get parts of date
                day = line_ind[0]
                line_ind.pop(0)

                month_s = line_ind[0]
                line_ind.pop(0)
                month = 0

                for i in range(len(months[lang])):
                    if month_s[:-1] == months[lang][i]:
                        month = i + 1
                        break

                year = line_ind[0]
                line_ind.pop(0)
                line_ind.pop(0)

                rel_index = Day.date_to_index(f'{day}/{month}/{year}', is_euro_date)

                day_path: str = ptrs_folders_path + str(rel_index[0])
                os.makedirs(day_path)

                print()
                print(f'writing {day} {months[2][month - 1]}, {year}...')

                with open(day_path + '/ptrs.txt', 'w') as file_day:
                    file_day.write(' '.join(line_ind) + '\n')

    @staticmethod
    def get_file_sha1_64bits(filepath: str) -> int:
        sha1 = hashlib.sha1()
        with open(filepath, 'rb') as f:
            # read the file in chunks to avoid memory issues with large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha1.update(chunk)

        # take the first 8 bytes (64 bits)
        full_hash = sha1.digest()
        hash_64_bit = int.from_bytes(full_hash[:8], byteorder='big')
        return hash_64_bit

    @staticmethod
    def get_directory_shasum(directory_path) -> int:
        shasum = 0
        for root, dirs, files in os.walk(directory_path):
            # skip hidden dirs/files like .git, .DS_Store, etc.
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

            for file in files:
                filepath = os.path.join(root, file)

                print(filepath)

                shasum += Sort.get_file_sha1_64bits(filepath)

        return shasum

