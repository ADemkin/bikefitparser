from db import Database
from generate_table import calculate_table_size
from generate_table import create_table
from os import remove
from os.path import exists


DBNAME='competitivecyclist_parsed.sqlite3'

def main():
    print('You about to create new db.')
    size_input = -1
    while size_input < 1:
        size_input = int(input('How many divisions for each parameter you want? '))
    size = calculate_table_size(size_input)
    print(f'Database size is going to be {size} rows')
    answer = input('Proceed? y/n: ')
    if answer not in ('y', 'Y'):
        exit()
    if exists(DBNAME):
        if input('Database already exist. Overwrite it? y/n: ') in ('y', 'Y'):
            remove(DBNAME)
        else:
            exit()
    print('Creating database... (may take some time)')
    table = create_table(size_input)
    db = Database(DBNAME)
    db.create()
    for row in table:
        db.insert_input_data(*row)
    actual_db_size = db.get_unprocessed_count()
    print(f'Created {DBNAME} database with {actual_db_size} rows')
    print('Now run main.py to start parsing')

if __name__ == '__main__':
    main()
