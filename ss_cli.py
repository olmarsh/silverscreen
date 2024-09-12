'''Command line manager for silverscreen databases.'''

import sqlite3
import database

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
O. Marsh      development version

Command line interface to manage the silverscreen movie database
This command line interface is not intended for end user use!
''')

conn = sqlite3.connect('silverscreen.db')
print('Connected to database\n')


def help():
    '''Read the help file and print it line by line'''

    print('''Reading help file
Press enter to read new lines
Press q then enter to quit
-----------------------------''')
    help_file = open('src/cli_help.txt', 'r')
    help_text = help_file.readlines()
    # Print the entire line except for the last character, which is a newline,
    # and wait for user input.
    for line in help_text:
        print(line[0:-1], end=' ')
        if input().lower() == 'q': break


def ninput(prompt, returntype=str):
    '''Normal input function that returns None when a blank string is input. \
       Return type can also be specified'''

    ret = input(prompt)

    # Return none if the input was blank.
    if ret == '': return None
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
INSERT - insert an entry into a table
DELETE - delete an entry from a table
UPDATE - update an entry in a table
SEARCH - search the movies database
VIEW   - print all entries from a table
LOGIN  - test logging in as a web user
EXIT   - exit the program''')
    action = input("What action to take?\n> ").lower()
    print('')

    if action == 'help':
        help()

    elif action == 'create':
        print('Create all tables if they do not exist')
        try:
            if database.db_create.create(conn):
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

    elif action == 'insert':
        print('Insert an entry into a table')
        table = input(
           'What table to input into? (Movies, Genres, AgeRatings, Users)\n> '
        ).lower()
        try:
            # Use appropriate column names depending on specified table
            if table == 'movies':
                print('Add new movie entry')
                if database.db_insert.insert(
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
                if database.db_insert.insert(
                    conn,
                    'Genres',
                    genre = ninput('Genre name:     '),
                    symbol = ninput('Unicode symbol: ')
                ):
                    conn.commit()
                    print('Operation completed successfully')
            elif table == 'ageratings' or table == 'age ratings':
                print('Add new age rating entry')
                if database.db_insert.insert(
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
                if database.db_insert.user_insert (
                    conn,
                    username = ninput('Username: '),
                    password = ninput('Password: ')
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
                'What table to delete from? (Movies, Genres, AgeRatings)\n> '
            ).lower()
            
            # Set the column to the correct name for the table.
            column = None
            if table == 'movies' or table == 'users':
                column = 'ID'
            elif table == 'genres':
                column = 'GenreID'
            elif table == 'ageratings':
                column = 'AgeRatingID'
            else:
                print('That table does not exist / hasn\'t been implemented yet')

            # If the table is valid, delete from it.
            if table in ('movies', 'genres', 'ageratings', 'users'):
                delete_id = input(f'Which {table} ID to delete?\n> ')
                print('Delete entry if exists')
                if database.db_delete.delete(conn, table, column, delete_id):
                    conn.commit();
                    print('Operation completed successfully')
        except Exception as error:
            format_error(error)

    elif action == 'update':
        try:

            table = input(
                'What table to update? (Movies, Users)\n> '
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
                    print('Operation completed successfully')

            elif table == 'users':
                # Take all inputs.
                edit_id = int(input('Which user ID to edit: '))
                print(f'Editing user ID {edit_id}')

                field = input('Which field to change \
(Username, Password, Admin): ')
                print(f'Editing field {field}')

                # Aid user in choosing between 1 and 0.
                if field.lower() == 'admin':
                    if input('Should this user have admin priveleges? y/N\n> ').lower() == 'y':
                        value = 1
                    else:
                        value = 0
                else:
                    value = input('What value to set the field to: ')
                print(f'Setting {field} to {value}')

                # Attempt to apply inputs to database.
                if database.db_update.update_user(conn, edit_id, {field: value}):
                    print('Operation completed successfully')
                    conn.commit()
        except Exception as error:
            format_error(error)

    elif action == 'view':
        try:
            table = input(
                'What table to view? (Movies, Genres, AgeRatings, Users)\n> '
            ).lower()

            # Use appropriate function depending on specified table
            if table == 'movies':
                if database.db_view.format_movies(
                    database.db_view.view_movies(conn)
                ):
                    print('Operation done successfully')
            elif table == 'genres' or table == 'ageratings' or table == 'users':
                if database.db_view.format_general(
                    database.db_view.view_general(conn, table)
                ):
                    print('Operation done successfully')
            else:
                print('Table doesn\'t exist / hasn\'t been implemented yet')
        except Exception as error:
            format_error(error)

    elif action == 'search':
        try:
            column = input('''Which column to search
(ID, Title, ReleaseYear, AgeRating, Runtime, Genre):
> ''')
            query = input('What is the search query: ')
            print('\nResults:')
            if database.db_view.format_movies(database.db_view.search_movies(conn, column, query)):
                    print('Operation done successfully')
        except Exception as error:
            format_error(error)

    elif action == 'login':
        try:
            username = input('Username: ')
            password = input('Password: ')

            conn = sqlite3.connect('silverscreen.db')
            
            user = database.db_login.authenticate(conn, username, password)

            # If the hash of the password matched the stored hash, authenticate the user.
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
