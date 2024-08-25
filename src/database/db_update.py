'''Update a specified entry from the movie database'''

import sqlite3


def update(conn, edit_id, fields):
    '''Update a specified entry in the movie database.

    Parameters:
    conn: Database connection object
    **kwargs: The column names followed by the value for this operation
              Use camelCase for these arguments, match the column name in
              the database exactly except the first letter must be lowercase

    '''

    cursor = conn.cursor()

    # If the field was genre or age rating, do the appropriate action with the
    # lookup table.
    for field, value in fields.items():
        try:
            if (field.lower() == 'genre'):
                cursor.execute(f'''SELECT * FROM Genres
                            WHERE Genre = \'{value.title()}\'''')
                field = 'GenreID'
                value = cursor.fetchone()[0]
                # print(f'Read genre id: {value}')
        except:  # Raise an exception if not found in lookup table
            raise Exception(f'ssLookupTableError: {value.title()} not a valid genre')
        try:
            if (field.lower() == 'agerating'):
                cursor.execute(f'''SELECT * FROM AgeRatings
                            WHERE AgeRating = \'{value.upper()}\'''')
                field = 'AgeRatingID'
                value = cursor.fetchone()[0]
                # print(f'Read age rating id: {value}')
        except:  # Raise an exception if not found in lookup table
            raise Exception(f'ssLookupTableError: {value.upper()} not a valid age rating')

        conn.execute(f'''UPDATE Movies SET
        {field} = '{value}'
        WHERE ID = {edit_id};
        ''')
    return True

if __name__ == '__main__':
    # Connect to database
    conn = sqlite3.connect('silverscreen.db')
    print('Connected to database')

    edit_id = int(input('Which movie ID to edit: '))
    print(f'Editing movie ID {edit_id}')

    field = input('''Which field to change
(Title, ReleaseYear, AgeRating, Runtime, Genre): ''')
    print(f'Editing field {field}')

    value = input('What value to set the field to: ')
    print(f'Setting {field} to {value}')

    if update(conn, edit_id, {field: value}):
        print('Operation completed successfully')

    conn.commit()
