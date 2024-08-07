'''Command line manager for silverscreen databases.'''

import sqlite3
from database import *

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
INSERT - insert an entry into a table
DELETE - delete an entry from a table
UPDATE - update an entry in a table
SEARCH - search the movies database
VIEW   - print all entries from a table''')
    action = input("What action to take?\n> ").lower()
    print('')
    if action == 'help':
        help()