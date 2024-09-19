'''Update a specified entry from the movie database'''

import sqlite3
import bcrypt


def update(conn, edit_id, fields):
    '''Update a specified entry in the movie database.'''

    cursor = conn.cursor()

    # If the field was genre or age rating, do the appropriate action with the
    # lookup table.
    for field, value in fields.items():
        if (field.lower() == 'genre'):
            cursor.execute(f'''SELECT * FROM Genres
                           WHERE Genre = \'{value.title()}\'''')
            field = 'GenreID'
            value = cursor.fetchone()[0]
            print(f'Read genre id: {value}')

        if (field.lower() == 'agerating'):
            cursor.execute(f'''SELECT * FROM AgeRatings
                           WHERE AgeRating = \'{value.upper()}\'''')
            field = 'AgeRatingID'
            value = cursor.fetchone()[0]
            print(f'Read age rating id: {value}')

    conn.execute(f'''UPDATE Movies SET
    {field} = '{value}'
    WHERE ID = {edit_id};
    ''')
    return True

def update_user(conn, edit_id, fields):
    '''Update information about a user in the database.'''

    for field, value in fields.items():

        # If the password is being updated, make sure it fits requirements.
        if field.lower() == 'password':
            password = value

            # Abort if the password is the wrong length
            if len(password) <= 12 or len(password) >= 50:
                raise Exception(f'Password length must be between 12 and 50 characters (Length: {len(password)})')

            # Abort if the password does not fulfil character requirements
            if not validate_password(password):
                raise Exception('Password must contain characters of: uppercase, lowercase, number and special')

            # Generate salt
            salt = bcrypt.gensalt()

            # Convert password to bytes and hash with salt
            value = bcrypt.hashpw(bytes(password, 'utf-8'), salt)

            conn.execute(f'''UPDATE Users SET
            {field} = ?
            WHERE ID = {edit_id};
            ''', (value.decode("utf-8"),)
            )

        else:  # For other values, hashing is not needed.
            conn.execute(f'''UPDATE Users SET
            {field} = '{value}'
            WHERE ID = {edit_id};
            ''')

    return True

def update_rating(conn, user_id, movie_id, value):
    '''Update a rating in the database.'''

    conn.execute(f'''UPDATE Ratings SET
    rating = '{value}'
    WHERE MovieID = {movie_id} AND UserID = {user_id};
    ''')

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


if __name__ == '__main__':
    # Connect to database
    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    print('Connected to database')

    table = input(
        'What table to update? (Movies, Users, Ratings)\n> '
    ).lower()

    if table.lower() == 'movies':
        edit_id = int(input('Which movie ID to edit: '))
        print(f'Editing movie ID {edit_id}')

        field = input('Which field to change \
(Title, ReleaseYear, AgeRating, Runtime, Genre): ')
        print(f'Editing field {field}')

        value = input('What value to set the field to: ')
        print(f'Setting {field} to {value}')

        if update(conn, edit_id, {field: value}):
            print('Updated if exists\nOperation completed successfully')
    elif table == 'users':
        edit_id = int(input('Which user ID to edit: '))
        print(f'Editing user ID {edit_id}')

        field = input('Which field to change \
(Username, Password, Admin): ')
        print(f'Editing field {field}')

        if field.lower() == 'admin':
            if input('Should this user have admin priveleges? y/N\n> ').lower() == 'y':
                value = 1
            else:
                value = 0
        else:
            value = input('What value to set the field to: ')
        print(f'Setting {field} to {value}')
        if update_user(conn, edit_id, {field: value}):
            print('Updated if exists\nOperation completed successfully')
            conn.commit()
    elif table == 'ratings':
        user_id = input('Which user ID to edit rating: ')
        movie_id = input('Which movie ID to edit favourite: ')
        rating = input('New rating value: ')
        if update_rating(conn, user_id, movie_id, rating):
            print('Updated if exists\nOperation completed successfully')
            conn.commit()
    else:
        print('That table does not exist / hasn\'t been implemented yet')