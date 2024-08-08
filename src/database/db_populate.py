'''Add the default values to the lookup tables.'''

import sqlite3

def populate(conn):
    '''Populate the genres and age ratings table if they are empty.'''

    # Populate genres table if it is empty
    if conn.execute('SELECT COUNT(*) FROM Genres').fetchall()[0][0] == 0:
        conn.execute('''INSERT INTO Genres (Genre, Symbol)
        VALUES
        ('Action','💣'),
        ('Animation', '🎞️'),
        ('Comedy', '😂'),
        ('Crime', '🔍'),
        ('Fantasy', '🪄')
        ''')
        print('Populated genres table')
    else:
        print('Genres table was not empty. Not populating')

    # Populate age ratings table if it is empty
    if conn.execute('SELECT COUNT(*) FROM AgeRatings').fetchall()[0][0] == 0:
        conn.execute('''INSERT INTO AgeRatings (AgeRating, MinAge, Description)
        VALUES
        ('G', 0, 'General Audiences'),
        ('PG', 0, 'Parental Guidance Suggested'),
        ('PG-13', 13, 'Parents Strongly Cautioned'),
        ('R', 17, 'Restricted'),
        ('NC-17', 17, 'Adults Only')
        ''')
        print('Populated age ratings table')
    else:
        print('Age ratings table was not empty. Not populating')

    return True;
    

if __name__ == '__main__':
    conn = sqlite3.connect('silverscreen.db')
    print('Connected to database')

    populate(conn)
    conn.commit()

    print('Operation completed successfully')
