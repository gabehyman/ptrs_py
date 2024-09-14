from day import Day


class Sort:

    def __init__(self, ptrs_path):
        self.days: list[Day] = []
        self.has_ptrs = False
        with open(ptrs_path, 'r') as file:
            for line in file:
                day: Day = Day(line.strip())
                self.days.append(day)

                # are there any pointers written
                if day.has_ptrs():
                    self.has_ptrs = True

