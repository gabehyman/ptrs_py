from day import Day
from user import User
import random as rand
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
