'''Command line manager for silverscreen databases.'''

import sqlite3
import database
import ss_import

# Print splash screen
print('''    ________   ________
   |\\   ____\\ |\\   ____\\ cli
   \\ \\  \\___|_\\ \\  \\___|_
    \\ \\_____  \\\\ \\_____  \\
     \\|____|\\  \\\\|____|\\  \\
       ____\\_\\  \\ ____\\_\\  \\
      |\\_________\\\\_________\\
      \\|_________\\|_________|
Silverscreen CLI database manager
O. Marsh          release version

Command line interface to manage the silverscreen movie database
This command line interface is for DATABASE MANAGEMENT PURPOSES
and is not intended for user use!

It will only be usable with reasonable training and reading of
the documentation (provided by HELP)

If you are an END USER, or WEB ADMIN, use the WEB INTERFACE.

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
''')

input('Press [Enter] to continue running the command line interface\n')

conn = sqlite3.connect('silverscreen.db')
conn.execute('PRAGMA foreign_keys = ON;')
print('Connected to database\n')


def help():
    '''Read the help file and print it line by line'''

    print('''Reading help file
Press >> enter << to read new lines
Type  >> q << then enter to quit
Type  >> g << and a number (i.e. g10) to Goto to a line
Type  >> j << and a number (i.e. j4, j-4) to Jump up/down lines (+/- allowed)
Type  >> p << and a number (i.e. p5) to print that many successive lines
--------------------------------------------------------------------------|----
'''[0:-1])
    help_file = open('cli_help.txt', 'r')
    help_text = help_file.readlines()
    # Print the entire line except for the last character, which is a newline,
    # and wait for user input.
    line = 0

    # Print the contents page
    for i in range(12):
        print(f'{(line+1):03d} {help_text[line][0:-1]:70}', end='|\n')
        line += 1  # Move to next line

    while True:
        print(f'{(line+1):03d}', end=' ')
        print(f'{help_text[line][0:-1]:70}', end=':')
        line += 1  # Move to next line

        # Take input for navigation commands
        command = input().lower()
        if command == '':
            command = 'n'

        if command[0] == 'q':  # Manage quitting the help function
            break
        elif command[0] == 'g':  # Manage jumping to a line
            try:
                line = int(command[1:])-1
                print('! Goto Line', command[1:])
            except TypeError:
                pass
        elif command[0] == 'j':  # Manage jumping forwards
            try:
                line = line+int(command[1:])-1
                print('! Jump', command[1:], 'Lines')
            except TypeError:
                pass
        elif command[0] == 'p':  # Manage printing successive lines
            try:
                for i in range(int(command[1:])-1):
                    print(f'{(line+1):03d} {help_text[line][0:-1]:70}',
                          end='|\n')
                    line += 1  # Move to next line
            except TypeError:
                pass
        # Limit the line number to within the text file's length
        if line < 0:
            line = 0
        if line > len(help_text)-1:
            line = len(help_text)-1


def ninput(prompt, returntype=str):
    '''Normal input function that returns None when a blank string is input. \
       Return type can also be specified'''

    ret = input(prompt)

    # Return none if the input was blank.
    if ret == '':
        return None
    # Convert to specified type and return.
    return returntype(ret)


def format_error(error):
    '''Format the error message nicely'''

    print('\n### ERROR ###')
    print(type(error).__name__+'\n'+str(error))
    print('#############')


# Main program
while True:
    # Print possible actions and get user's choice
    print('''Choose an action:
HELP   - read help documentation for CLI
CREATE - attempt to create all tables in the database
DROP   - drop a table or multiple tables from the database
PPLATE - populate the lookup tables with default values
IMPORT - import the default movies into the table
INSERT - insert an entry into a table
DELETE - delete an entry from a table   by ID
UPDATE - update an entry in a table     by ID
SEARCH - search a table                 by any column
VIEW   - print all entries from a table
LOGIN  - test logging in as a web user  by username
EXIT   - exit the program''')
    action = input("What action to take?\n> ").lower()
    print('')

    if action == 'help':
        help()

    elif action == 'create':
        print('Create all tables if they do not exist')
        try:
            if database.db_create.create_users(conn) \
                    and database.db_create.create(conn):
                print('Operation completed successfully')
        except Exception as error:
            format_error(error)

    elif action == 'drop':
        print('Drop table(s) - type \'ALL\' to drop all tables')
        try:
            table = input('Which table to drop: ').title()
            if database.db_drop.drop_table(conn, table):
                print('Operation completed successfully')
        except Exception as error:
            format_error(error)

    elif action == 'pplate':
        print('Populate the tables with the default values')
        if database.db_populate.populate(conn):
            conn.commit()
            print('Operation completed successfully')

    elif action == 'import':
        try:
            ss_import.import_default_list(conn)
        except Exception as error:
            format_error(error)

    elif action == 'insert':
        print('Insert an entry into a table')
        table = input(
           'What table to input into? (Movies, Genres, AgeRatings, Users, \
Ratings, Favourites)\n> '
        ).lower()
        try:
            # Use appropriate column names depending on specified table
            if table == 'movies':
                print('Add new movie entry')
                if database.db_insert.insert(
                    conn,
                    'Movies',
                    title=ninput('Movie title:  '),
                    releaseYear=ninput('Release year: ', int),
                    ageRating=ninput('Age rating:   '),
                    runtime=ninput('Runtime:      ', int),
                    genre=ninput('Genre:        ')
                ):
                    conn.commit()
                    print('Operation completed successfully')
            elif table == 'genres':
                print('Add new genre entry')
                if database.db_insert.insert(
                    conn,
                    'Genres',
                    genre=ninput('Genre name:     '),
                    symbol=ninput('Unicode symbol: ')
                ):
                    conn.commit()
                    print('Operation completed successfully')
            elif table == 'ageratings' or table == 'age ratings':
                print('Add new age rating entry')
                if database.db_insert.insert(
                    conn,
                    'AgeRatings',
                    ageRating=ninput('Age Rating:  '),
                    minAge=ninput('Minimum Age: '),
                    description=ninput('Description: ')
                ):
                    conn.commit()
                    print('Operation completed successfully')
            elif table == 'users':
                print('Add new user')
                if database.db_insert.user_insert(
                    conn,
                    username=ninput('Username: '),
                    password=ninput('''\nPassword limitations:
12 characters
Must contain uppercase, lowercase, number and special character\n
Password: ''')
                ):
                    conn.commit()
                    print('Operation completed successfully')
            elif table == 'ratings':
                print('Insert a rating')
                if database.db_insert.rating_insert(
                    conn,
                    user_id=ninput('User ID: '),
                    movie_id=ninput('Movie ID: '),
                    rating=ninput('Rating: ')
                ):
                    conn.commit()
                    print('Operation completed successfully')
            elif table == 'favourites':
                print('Add new favourite')
                if database.db_insert.favourite_insert(
                    conn,
                    user_id=ninput('User ID: '),
                    movie_id=ninput('Movie ID: ')
                ):
                    conn.commit()
                    print('Operation completed successfully')
            else:
                print('That table does not exist / hasn\'t been implemented \
yet')
        except Exception as error:
            format_error(error)

    elif action == 'delete':
        try:
            table = input(
                'What table to delete from? (Movies, Genres, AgeRatings, \
Users, Ratings, Favourites)\n> '
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
                print('That table does not exist / hasn\'t been implemented \
yet')

            # If the table is valid, delete from it.
            if table in ('movies', 'genres', 'ageratings', 'users', 'ratings',
                         'favourites'):
                delete_id = input(f'Which {table} ID to delete?\n> ')
                print('Delete entry if exists')
                if database.db_delete.delete(conn, table, column, delete_id):
                    conn.commit()
                    print('Operation completed successfully')

        except Exception as error:
            format_error(error)

    elif action == 'update':
        try:

            table = input(
                'What table to update? (Movies, Users, Ratings)\n> '
            ).lower()

            if table.lower() == 'movies':
                # Take all inputs.
                edit_id = int(input('Which movie ID to edit: '))
                print(f'Editing movie ID {edit_id}')

                field = input('Which field to change \
(Title, ReleaseYear, AgeRating, Runtime, Genre): ')
                print(f'Editing field {field}')

                value = input('What value to set the field to: ')
                print(f'Setting {field} to {value}')

                # Attempt to apply them to database.
                if database.db_update.update(conn, edit_id, {field: value}):
                    print('Updated if exists\nOperation completed successfully'
                          )

            elif table == 'users':
                # Take all inputs.
                edit_id = int(input('Which user ID to edit: '))
                print(f'Editing user ID {edit_id}')

                field = input('Which field to change \
(Username, Password, Admin): ')
                print(f'Editing field {field}')

                # Aid user in choosing between 1 and 0.
                if field.lower() == 'admin':
                    if input('Should this user have admin priveleges? y/N\n> '
                             ).lower() == 'y':
                        value = 1
                    else:
                        value = 0
                else:
                    value = input('What value to set the field to: ')
                print(f'Setting {field} to {value}')

                # Attempt to apply inputs to database.
                if database.db_update.update_user(conn, edit_id,
                                                  {field: value}):
                    print('''Updated if exists
Operation completed successfully''')
                    conn.commit()

            elif table == 'ratings':
                user_id = input('Which user ID to edit rating: ')
                movie_id = input('Which movie ID to edit favourite: ')
                rating = input('New rating value: ')
                if database.db_update.update_rating(conn, user_id, movie_id,
                                                    rating):
                    print('''Updated if exists
Operation completed successfully''')
                    conn.commit()
            else:
                print('That table does not exist / hasn\'t been implemented \
yet')
        except Exception as error:
            format_error(error)

    elif action == 'view':
        try:
            table = input(
                'What table to view? (Movies, Genres, AgeRatings, Users, \
Ratings, Favourites)\n> '
            ).lower()

            # Use appropriate function depending on specified table
            if table == 'movies':
                if database.db_view.format_movies(
                    database.db_view.view_movies(conn)
                ):
                    print('Operation done successfully')
            elif table in ('genres', 'ageratings', 'users'):
                if database.db_view.format_general(
                    database.db_view.view_general(conn, table)
                ):
                    print('Operation done successfully')
            elif table in ('ratings', 'favourites'):
                if database.db_view.format_favourites_ratings(
                    database.db_view.view_general(conn, table),
                    table_type=table
                ):
                    print('Operation done successfully')
            else:
                print('Table doesn\'t exist / hasn\'t been implemented yet')
        except Exception as error:
            format_error(error)

    elif action == 'search':
        try:
            table = input(
                'What table to search? (Movies, Genres, AgeRatings, Users, \
Ratings, Favourites)\n> '
            ).lower()
            if table == 'movies':
                # Take inputs for movies table and search.
                column = input('''Which column to search
(ID, Title, ReleaseYear, AgeRating, Runtime, Genre):
> ''')
                query = input('What is the search query: ')
                print('\nResults:')
                if database.db_view.format_movies(
                    database.db_view.search_movies(conn, column, query)
                ):
                    print('Operation done successfully')
            elif table == 'users':
                column = input('''Which column to search
(ID, Username, Admin):
> ''')
                query = input('What is the search query: ')
                print('\nResults:')
                if database.db_view.format_users(
                    database.db_view.search_users(conn, column, query)
                ):
                    print('Operation done successfully')

            # Search for either favourites or ratings
            elif table == 'ratings' or table == 'favourites':
                # Specify what to search for
                user_id = ninput(f'Which user ID to view {table} for \
(blank for all users): ')
                movie_id = ninput('Which movie ID to search \
(blank for all movies): ')
                print('\nResults:')
                if database.db_view.format_favourites_ratings(
                    database.db_view.search_favourites_ratings(
                        conn, table, user_id, movie_id
                    ),
                    table_type=table
                ):
                    print('Operation done successfully')
            else:
                print('Table doesn\'t exist / hasn\'t been implemented yet')
        except Exception as error:
            format_error(error)

    elif action == 'login':
        try:
            username = input('Username: ')
            password = input('Password: ')

            user = database.db_login.authenticate(conn, username, password)

            # If the hash of the password matched the stored hash,
            # authenticate the user.
            if user:
                print('Login Successful')
                print(user[1])
            else:
                print('Login Unsuccessful')
        except Exception as error:
            format_error(error)

    elif action == 'exit':
        break

    else:
        print('That action does not exist / hasn\'t been implemented yet')

    input('\nPress [ENTER] to continue...\n')
