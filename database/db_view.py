'''Print all tables from the database.'''

import sqlite3


def format_movies(results):
    '''Format the output from the view_movies or search_movies function.'''


    # Define line spacings
    formatted_row = '{:<5} {:<25} {:<13} {:<10} {:<16} {:<12} {:<15} {}'
    # Print column headers, then the rest of the rows
    print(formatted_row.format('ID', 'Title', 'Release Year', 'Runtime',
                               'Genre', 'Age Rating', 'Average Rating', 'Favourites'))
    for row in results:
        # Remove unneccessary results
        cut_row = list(row[0:6])
        if row[9] == None:
            cut_row.append('-')
        else:
            cut_row.append(f'{row[9]} ({row[10]} ratings)')
        if row[11] == None:
            cut_row.append('-')
        else:
            cut_row.append(row[11])
        print(formatted_row.format(*cut_row))

    # Add newline at bottom
    print('')
    return True

def format_users(results):
    '''Format the output from the view_movies or search_movies function.'''

    # Define line spacings
    formatted_row = '{:<5} {:<30} {:<65} {:<10}'
    # Print column headers, then the rest of the rows
    print(formatted_row.format('ID', 'Username', 'Password hash', 'Admin?'))
    for row in results:
        print(formatted_row.format(*row))

    # Add newline at bottom
    print('')
    return True


def format_favourites_ratings(results, table_type = 'ratings'):
    '''Format the output from a favourites or ratings search function.'''

    # Define line spacings
    formatted_row = '{:<5} {:<10} {:<10}'
    # Add the extra row for ratings if needed
    if table_type == 'ratings':
        formatted_row += ' {:<5}'

    # Print column headers, then the rest of the rows
    print(formatted_row.format('ID', 'User ID', 'Movie ID', 'Rating'))
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
    AgeRating, Symbol, MinAge, Description,
    (SELECT AVG(Ratings.Rating)
        FROM Ratings 
        WHERE Ratings.MovieID = Movies.ID
    ),
    (SELECT Count(Ratings.Rating)
        FROM Ratings 
        WHERE Ratings.MovieID = Movies.ID
    ),
    (SELECT Count(Favourites.MovieID)
        FROM Favourites 
        WHERE Favourites.MovieID = Movies.ID
    ) FROM Movies
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
    '''Return the selected table.'''

    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM {table}''')
    return cursor.fetchall()

def search_users(conn, column, query, limit=0, offset=0, order='ID ASC',
                   match_before = True, match_after = True):
    '''Search for a user in the users table by specified column.'''

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
    cursor.execute(f'''SELECT ID, Username, Password, Admin FROM Users
    WHERE {column} LIKE {match_before_string} '{query}' {match_after_string}
    ORDER BY {order}
    {extra}''')
    return cursor.fetchall()

def search_favourites_ratings(conn, table, user_id=None, movie_id=None, limit=0, offset=0):
    '''Search for ratings/favourites in the ratings/favourites table by user id, movie id.'''

    # Add extra parameters to query.
    extra = ''
    if limit > 0:
        extra += f'LIMIT {limit}'
        if offset != '' and offset > 0:
            extra += f' OFFSET {offset}'
        extra += ';'

    # Add appropriate search parameters
    params = ''
    if user_id or movie_id:
        params += 'WHERE '
    if user_id:
        params += f'UserID = \'{user_id}\' '
    if movie_id:
        params += f'MovieID = \'{movie_id}\' '


    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM {table}
    {params}
    {extra}''')
    return cursor.fetchall()
    

def search_movies(conn, column, query, limit=0, offset=0, order='ID ASC',
                  match_before = True, match_after = True,
                  get_favourites = False, user = None):
    '''Search for a movie in the movies table by specified column.'''

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
    AgeRating, Symbol, MinAge, Description,
    (SELECT AVG(Ratings.Rating)
        FROM Ratings 
        WHERE Ratings.MovieID = Movies.ID
    ),
    (SELECT Count(Ratings.Rating)
        FROM Ratings 
        WHERE Ratings.MovieID = Movies.ID
    ),
    (SELECT Count(Favourites.MovieID)
        FROM Favourites 
        WHERE Favourites.MovieID = Movies.ID
    ) FROM Movies
    INNER JOIN Genres ON Movies.GenreID = Genres.GenreID
    INNER JOIN AgeRatings ON Movies.AgeRatingID = AgeRatings.AgeRatingID
    WHERE {column} LIKE {match_before_string} '{query}' {match_after_string}
    ORDER BY {order}
    {extra}''')
    return cursor.fetchall()


if __name__ == '__main__':
    # Only define the function if it is being run as main.
    def ninput(prompt, returntype=str):
        '''Normal input function that returns None when a blank string is input. \
        Return type can also be specified'''

        ret = input(prompt)

        # Return none if the input was blank.
        if ret == '': return None
        # Convert to specified type and return.
        return returntype(ret)

    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    print('Connected to database')

    # Print possible actions and get user's choice
    print('''Choose an action:
SEARCH - search the movies or users table
VIEW   - print all entries from a table''')
    action = input('What action to take?\n> ').lower()
    print('')
    if action == 'view':
        table = input(
            'What table to view? (Movies, Genres, AgeRatings, Users, Ratings, Favourites)\n> '
        ).lower()

        # Use appropriate function depending on specified table
        if table == 'movies':
            if format_movies(view_movies(conn)):
                print('Operation done successfully')
        elif table in ('genres', 'ageratings', 'users'):
            if format_general(view_general(conn, table)):
                print('Operation done successfully')
        elif table in ('ratings', 'favourites'):
            if format_favourites_ratings(view_general(conn, table), table_type=table):
                print('Operation done successfully')
        else:
            print('Table doesn\'t exist / hasn\'t been implemented yet')

    elif action == 'search':
        table = input(
            'What table to search? (Movies, Users, Ratings, Favourites)\n> '
        ).lower()

        if table == 'movies':
            # Take inputs for movies table and search.
            column = input('''Which column to search
(ID, Title, ReleaseYear, AgeRating, Runtime, Genre):
> ''')
            query = input('What is the search query: ')
            print('\nResults:')
            if format_movies(search_movies(conn, column, query)):
                    print('Operation done successfully')
        if table == 'users':
            column = input('''Which column to search
(ID, Username, Admin):
> ''')
            query = input('What is the search query: ')
            print('\nResults:')
            if format_users(search_users(conn, column, query)):
                print('Operation done successfully')

        # Search for either favourites or ratings
        if table == 'ratings' or table == 'favourites':
            # Specify what to search for
            user_id = ninput(f'Which user ID to view {table} for (blank for all users): ')
            movie_id = ninput('Which movie ID to search (blank for all movies): ')
            print('\nResults:')
            if format_favourites_ratings(search_favourites_ratings(conn, table, user_id, movie_id), table_type=table):
                print('Operation done successfully')
        else:
            print('Table doesn\'t exist / hasn\'t been implemented yet')

    else:
        print('That action does not exist for this module')
