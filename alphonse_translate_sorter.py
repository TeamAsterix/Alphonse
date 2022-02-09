

from alphonseecem.translator import get_language_files, pwd
from json import dumps, loads


def sort_json(filename):
    json = f'{pwd}/{filename}'
    load = {}

    with open(json, 'r+') as jfile:
        load = loads(jfile.read())

    dump = dumps(load, indent=4, sort_keys=True)
    with open(json, 'w+') as jfile:
        jfile.write(dump)


for i in get_language_files():
    print(f'Sorting {i} ...')
    sort_json(i)
    print(f'Sorted {i}!')

print('All jobs completed successfully!')
