'''Add an entry to a silverscreen database'''

import sqlite3

def insert(conn, table, **kwargs):
    '''Insert into the table based on the specified keyword arguments.
    
    Parameters:
    conn: Database connection object
    table: The table to insert into
    **kwargs: The column names followed by the value for this operation
              Use camelCase for these arguments, match the column name in
              the database exactly except the first letter must be lowercase'''

    print('Read keyword arguments', kwargs)
    cursor = conn.cursor()

    # Remove NoneTypes from kwargs
    to_remove = {}

    for kwarg in kwargs:
        if kwargs[kwarg] == None:
            to_remove[kwarg] = kwargs
    for kwarg in to_remove:
        kwargs.pop(kwarg)

    # Get genre ID if genre was given, write it to kwargs.
    if 'genre' in kwargs and table == 'Movies':
        cursor.execute(f'''SELECT * FROM Genres
                           WHERE Genre = \'{kwargs['genre'].title()}\'''')
        
        kwargs['genreID'] = cursor.fetchone()[0]
        print(f'Read genre id: {kwargs['genreID']}')

    # Get age rating ID if age rating was given, write it to kwargs.
    if 'ageRating' in kwargs and table == 'Movies':
        cursor.execute(f'''SELECT * FROM AgeRatings
                           WHERE AgeRating = \'{kwargs['ageRating'].upper()}\'
                           ''')
        
        kwargs['ageRatingID'] = cursor.fetchone()[0]
        print(f'Read age rating id: {kwargs['ageRatingID']}')

    # Pop both genre and age rating arguments
    try:
        kwargs.pop('genre')
    except KeyError:
        pass
    
    try:
        kwargs.pop('ageRating')
    except KeyError:
        pass

    # Insert the arguments into the specified table by formatting them as
    # comma separated strings of keys and values
    conn.execute(f'''INSERT INTO {table} (
        {str(list(kwargs.keys()))[1:-1]}
    )
    VALUES (
        {str(list(kwargs.values()))[1:-1]}
    );''')

    return True

# If this program is run in terminal, execute its function.
if __name__ == '__main__':

    # Connect to database
    conn = sqlite3.connect('silverscreen.db')
    cursor = conn.cursor()
    print('Connected to database')

    # Get user inputs for new movie
    print('Add new movie to database')
    title = input('Movie title:  ')
    releaseYear = int(input('Release year: '))
    ageRating = input('Age rating:   ')
    runtime = int(input('Runtime:      '))
    genre = input('Genre:        ')

    conn.commit()

    print('Operation done successfully')
