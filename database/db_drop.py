'''Drop a specified table from the database.'''

import sqlite3

def drop_table(conn, table):
    '''Drop the table from the database.'''

    # Drop all tables and return the result
    if table == 'All':
        return drop_all_tables(conn)
    
    conn.execute(f'DROP TABLE {table}')
    return True

def drop_all_tables(conn):
    '''Drop all tables from the database.'''

    conn.execute('DROP TABLE IF EXISTS AgeRatings')
    conn.execute('DROP TABLE IF EXISTS Genres')
    conn.execute('DROP TABLE IF EXISTS Movies')
    conn.execute('DROP TABLE IF EXISTS Users')
    conn.execute('DROP TABLE IF EXISTS Ratings')
    conn.execute('DROP TABLE IF EXISTS Favourites')
    return True

# If this program is run in terminal, execute its function.
if (__name__ == '__main__'):
    conn = sqlite3.connect('silverscreen.db')
    print('Connected to database')

    print('Drop table(s) - type \'ALL\' to drop all tables')
    if drop_table(conn, input('Which table to drop: ').title()):
        print('Operation completed successfully')