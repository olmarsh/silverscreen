'''Print all tables from the database.'''

import sqlite3


def format_movies(results):
    '''Format the output from the view_movies or search_movies function.'''

    # Define line spacings
    formatted_row = '{:<5} {:<25} {:<13} {:<10} {:<16} {:<6}'
    # Print column headers, then the rest of the rows
    print(formatted_row.format('ID', 'Title', 'Release Year', 'Runtime',
                               'Genre', 'Age Rating'))
    for row in results:
        print(formatted_row.format(*row))

    # Add newline at bottom
    print('')
    return True


def format_general(results):
    '''Format the output from a view or search function.'''

    for row in results:
        print(*row, sep=', ')

    # Add newline at bottom
    print('')
    return True


def view_movies(conn, limit=0, offset=0, order='ID ASC'):
    '''Return the entire movies table.'''

    # Add extra parameters to query.
    extra = ''
    if limit > 0:
        extra += f'LIMIT {limit}'
        if offset != '' and offset > 0:
            extra += f' OFFSET {offset}'
        extra += ';'

    # Select all from table and return them.
    cursor = conn.cursor()
    cursor.execute(f'''SELECT ID, Title, ReleaseYear, Runtime, Genre,
                   AgeRating, Symbol, MinAge, Description FROM Movies
    INNER JOIN Genres ON Movies.GenreID = Genres.GenreID
    INNER JOIN AgeRatings on Movies.AgeRatingID = AgeRatings.AgeRatingID
    ORDER BY {order}
    {extra}''')
    return cursor.fetchall()

def count_movies(conn, column='Title', query='', match_before = True,
                 match_after = True):
    '''Return the number of entries in the movies table.'''

    # Whether to return queries with matches before or after the string
    match_before_string = ''
    if match_before:
        match_before_string = '\'%\' ||'

    match_after_string = ''
    if match_after:
        match_after_string = '|| \'%\''

    cursor = conn.cursor()
    cursor.execute(f'''SELECT COUNT(*) FROM Movies
    INNER JOIN Genres ON Movies.GenreID = Genres.GenreID
    INNER JOIN AgeRatings on Movies.AgeRatingID = AgeRatings.AgeRatingID
    WHERE {column} LIKE {match_before_string} '{query}' {match_after_string}
                   ''')

    return cursor.fetchone()[0]


def view_general(conn, table):
    '''Return the selected table'''
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM {table}''')
    return cursor.fetchall()


def search_movies(conn, column, query, limit=0, offset=0, order='ID ASC',
                  match_before = True, match_after = True):
    '''Search for a movie in the movies table by specified column'''

    # Add extra parameters to query.
    extra = ''
    if limit > 0:
        extra += f'LIMIT {limit}'
        if offset != '' and offset > 0:
            extra += f' OFFSET {offset}'
        extra += ';'

    # Whether to return queries with matches before or after the string
    match_before_string = ''
    if match_before:
        match_before_string = '\'%\' ||'
    
    match_after_string = ''
    if match_after:
        match_after_string = '|| \'%\''

    cursor = conn.cursor()
    cursor.execute(f'''SELECT ID, Title, ReleaseYear, Runtime, Genre,
                   AgeRating, Symbol, MinAge, Description FROM Movies
    INNER JOIN Genres ON Movies.GenreID = Genres.GenreID
    INNER JOIN AgeRatings on Movies.AgeRatingID = AgeRatings.AgeRatingID
    WHERE {column} LIKE {match_before_string} '{query}' {match_after_string}
    ORDER BY {order}
    {extra}''')
    return cursor.fetchall()


if __name__ == '__main__':
    conn = sqlite3.connect('silverscreen.db')
    print('Connected to database')

    # Print possible actions and get user's choice
    print('''Choose an action:
SEARCH - search the movies database
VIEW   - print all entries from a table''')
    action = input('What action to take?\n> ').lower()
    print('')
    if action == 'view':
        table = input(
            'What table to view? (Movies, Genres, AgeRatings)\n> '
        ).lower()

        # Use appropriate function depending on specified table
        if table == 'movies':
            if format_movies(view_movies(conn)):
                print('Operation done successfully')
        elif table == 'genres' or table == 'ageratings':
            if format_general(view_general(conn, table)):
                print('Operation done successfully')
        else:
            print('Table doesn\'t exist / hasn\'t been implemented yet')

    elif action == 'search':
        column = input('''Which column to search
(ID, Title, ReleaseYear, AgeRating, Runtime, Genre):
> ''')        
        query = input('What is the search query: ')
        print('\nResults:')
        if format_movies(search_movies(conn, column, query)):
                print('Operation done successfully')
    else:
        print('That action does not exist for this module')
