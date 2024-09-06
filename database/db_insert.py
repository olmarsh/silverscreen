'''Add an entry to a silverscreen database, users or movies'''

import sqlite3
import bcrypt

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


def user_insert(conn, username, password):
    '''Hash the user's password and insert a the user into the database.'''

    # Abort if the password is the wrong length
    if len(password) <= 12 or len(password) >= 50:
        raise Exception(f'Password length must be between 12 and 50 characters (Length: {len(password)})')

    # Abort if the password does not fulfil character requirements
    if not validate_password(password):
        raise Exception('Password must contain characters of: uppercase, lowercase, number and special')

    # Generate salt
    salt = bcrypt.gensalt()

    # Convert password to bytes and hash with salt
    hash = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
    
    # Insert username and hashed password bytes into table
    conn.execute(f'''INSERT INTO Users (
        Username, Password
    )
    VALUES (
        '{username}', ?
        );''',
        (hash.decode("utf-8"),)
    )

    return True


def validate_password(password):
    '''Returns true if a password meets special character requirements.'''
    
    # Set all requirements to false
    lower, upper, num, special = (False,)*4

    special_characters = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

    # If a requirement is met, set it to true
    for i in password:
        if i == i.lower():
            lower = True
        if i == i.upper():
            upper = True
        if i.isdigit:
            num = True
        if i in special_characters:
            special = True

    return lower and upper and num and special;

# If this program is run in terminal, execute its function.
if __name__ == '__main__':

    def ninput(prompt, returntype=str):
        '''Normal input function that returns None when a blank string is \
           input.
           Return type can also be specified'''

        ret = input(prompt)

        # Return none if the input was blank.
        if ret == '': return None
        # Convert to specified type and return.
        return returntype(ret)

    # Connect to database
    conn = sqlite3.connect('silverscreen.db')
    cursor = conn.cursor()
    print('Connected to database')

    # Get user inputs for new entry
    print('Insert an entry into a table')
    table = input(
        'What table to input into? (Movies, Genres, AgeRatings, Users)\n> '
    ).lower()
    # Use appropriate column names depending on specified table
    if table == 'movies':
        print('Add new movie entry')
        if insert(
            conn,
            'Movies',
            title = ninput('Movie title:  '),
            releaseYear = ninput('Release year: ',int),
            ageRating = ninput('Age rating:   '),
            runtime = ninput('Runtime:      ', int),
            genre = ninput('Genre:        ')
        ):
            conn.commit()
            print('Operation completed successfully')
    elif table == 'genres':
        print('Add new genre entry')
        if insert(
            conn,
            'Genres',
            genre = ninput('Genre name:     '),
            symbol = ninput('Unicode symbol: ')
        ):
            conn.commit()
            print('Operation completed successfully')
    elif table == 'ageratings' or table == 'age ratings':
        print('Add new age rating entry')
        if insert(
            conn,
            'AgeRatings',
            ageRating = ninput('Age Rating:  '),
            minAge = ninput('Minimum Age: '),
            description = ninput('Description: ')
        ):
            conn.commit()
            print('Operation completed successfully')
    elif table == 'users':
        print('Add new user')
        if user_insert (
            conn,
            username = ninput('Username: '),
            password = ninput('Password: ')
        ):
            conn.commit()
            print('Operation completed successfully')
    else:
        print('That table does not exist / hasn\'t been implemented \
                yet')
