'''Delete an entry from a database.'''

import sqlite3


def delete(conn, table, match_column, delete_id):
    '''Delete the selected ID from the selected table'''

    conn.execute(f'''DELETE FROM {table}
    WHERE {match_column} = {delete_id};
    ''')
    return True


if __name__ == '__main__':
    conn = sqlite3.connect("silverscreen.db")
    conn.execute('PRAGMA foreign_keys = ON;')
    print("Connected to database")
    table = input(
        'What table to delete from? \
(Movies, Genres, AgeRatings, Users, Ratings, Favourites)\n> '
    ).lower()

    # Set the column to the correct name for the table.
    column = None
    if table == 'movies' or table == 'users':
        column = 'ID'
    elif table == 'genres':
        column = 'GenreID'
    elif table == 'ageratings':
        column = 'AgeRatingID'
    elif table == 'ratings':
        column = 'RatingID'
    elif table == 'favourites':
        column = 'FavouriteID'
    else:
        print('That table does not exist / hasn\'t been implemented yet')

    # If the table is valid, delete from it.
    if table in ('movies', 'genres', 'ageratings', 'users', 'ratings',
                 'favourites'):
        delete_id = input(f'Which {table} ID to delete?\n> ')
        print('Delete entry if exists')
        if delete(conn, table, column, delete_id):
            conn.commit()
            print('Operation completed successfully')
