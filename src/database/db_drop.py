'''Drop a specified table from the database.'''

import sqlite3

def drop_table(conn, table):
    conn.execute(f'DROP TABLE {table}')
    return True

conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

if (__name__ == '__main__'):
    drop_table(conn, input('Which table to drop: '))