'''Imports the database values from the default_films.txt file'''

import database


def import_default_list(conn):
    '''Import the default list into the table.'''
    # Open the films file and read its contents into a variable.
    file = open('default_films.txt', 'r')
    text = file.readlines()

    print('Importing movies from default_films.txt')
    preserve = input('Preserve movie ID from text file? (y/N/cancel)\n> ')\
        .lower()

    if preserve == 'y':
        # For every film, parse it, and insert it into the database.
        for line in text:
            parsed_line = line[0:-1].split(',')
            print(parsed_line)
            if database.db_insert.insert(
                conn,
                'Movies',
                id=parsed_line[0],
                title=parsed_line[1],
                releaseYear=parsed_line[2],
                ageRating=parsed_line[3],
                runtime=parsed_line[4],
                genre=parsed_line[5]
            ):
                print('Imported', parsed_line[1], '\n')
            conn.commit()
        print('Operation completed successfully')
    elif preserve == 'n':
        # Same program but ID is allowed to increment automatically.
        for line in text:
            parsed_line = line[0:-1].split(',')
            print(parsed_line)
            if database.db_insert.insert(
                conn,
                'Movies',
                title=parsed_line[1],
                releaseYear=parsed_line[2],
                ageRating=parsed_line[3],
                runtime=parsed_line[4],
                genre=parsed_line[5]
            ):
                print('Imported', parsed_line[1], '\n')
        conn.commit()
        print('Operation completed successfully')
    elif preserve == 'c' or preserve == 'cancel':
        print('Cancelled')
    else:
        print('Not a valid input')


if __name__ == '__main__':
    import sqlite3
    import database.db_insert

    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')

    print('Connected to database\n')
    import_default_list(conn)
