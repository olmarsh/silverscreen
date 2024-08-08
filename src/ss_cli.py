'''Command line manager for silverscreen databases.'''

import sqlite3
import database.db_create
import database.db_drop
import database.db_populate
#import database.db_delete
#import database.db_insert
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

# Main program
while True:
    # Print possible actions and get user's choice
    print('''Choose an action:
HELP   - read help documentation for CLI
CREATE - attempt to create all tables in the database
DROP   - drop a table or multiple tables from the database
PPLATE - populate the lookup tables with default values
# INSERT - insert an entry into a table
# DELETE - delete an entry from a table
# UPDATE - update an entry in a table
# SEARCH - search the movies database
# VIEW   - print all entries from a table''')
    action = input("What action to take?\n> ").lower()
    print('')

    if action == 'help':
        help()

    if action == 'create':
        print('Create all tables if they do not exist')
        if database.db_create.create(conn):
            print('Operation completed successfully')

    if action == 'drop':
        print('Drop table(s) - type \'ALL\' to drop all tables')
        table = input('Which table to drop: ').title()
        if database.db_drop.drop_table(conn, table):
            print('Operation completed successfully')

    if action == 'pplate':
        print('Populate the tables with the default values')
        if database.db_populate.populate(conn):
            conn.commit()
            print('Operation completed successfully')

    input('Press enter to continue...\n')
