'''Update a specified entry from the movie database'''

import sqlite3


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
            print('Operation completed successfully')
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
            print('Operation completed successfully')
            conn.commit()
    elif table == 'ratings':
        user_id = input('Which user ID to edit rating: ')
        movie_id = input('Which movie ID to edit favourite: ')
        rating = input('New rating value: ')
        if update_rating(conn, user_id, movie_id, rating):
            print('Operation completed successfully')
            conn.commit()
    else:
        print('That table does not exist / hasn\'t been implemented yet')