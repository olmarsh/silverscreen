'''Command line manager for silverscreen databases.'''

import sqlite3
import database.db_create
import database.db_drop
import database.db_populate
import database.db_insert
#import database.db_delete
#import database.db_update
#import database.db_view


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
Oliver M.     development version

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
# DELETE - delete an entry from a table
# UPDATE - update an entry in a table
# SEARCH - search the movies database
# VIEW   - print all entries from a table
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
           'What table to input into? (Movies, Genres, AgeRatings)\n> '
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
            else:
                print('That table does not exist / hasn\'t been implemented \
                      yet')
        except Exception as error:
            format_error(error)

    elif action == 'exit':
        break
    
    else:
        print('That action does not exist / hasn\'t been implemented yet')

    input('\nPress enter to continue...\n[ENTER]')
