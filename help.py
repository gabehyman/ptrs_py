from sort import Sort

months: list[list[str]] = [
        ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
         'december'],
        ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
         'deciembre'],
        ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november',
         'december']]

ptrs_folders_path: str = '/Users/gabehyman/Downloads/ptrs_py_fake/'
ptrs_file_path: str = '/Users/gabehyman/Downloads/pters.txt'

# Sort.ptrs_file_to_folder(ptrs_file_path, ptrs_folders_path, months, 2, True)

x = Sort.get_directory_shasum('/Users/gabehyman/dev/ptrs_py/ptrs')
print(x)
y = 16549938407955204857383
print(x == y)
print(abs(x - y))

