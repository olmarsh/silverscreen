'''Create the silverscreen database, add movie/user table and lookup tables.'''

import sqlite3

def create(conn):
    '''Create silverscreen movie table and lookup tables.'''

    # Create genre lookup table
    conn.execute('''CREATE TABLE IF NOT EXISTS Genres (
    GenreID INTEGER PRIMARY KEY,
    Genre TEXT NOT NULL,
    Symbol TEXT
    );''')

    # Create age rating lookup table
    conn.execute('''CREATE TABLE IF NOT EXISTS AgeRatings (
    AgeRatingID INTEGER PRIMARY KEY,
    AgeRating TEXT NOT NULL,
    MinAge INTEGER NOT NULL,
    Description TEXT
    );''')

    # Create movies table
    conn.execute('''CREATE TABLE IF NOT EXISTS Movies (
        ID INTEGER PRIMARY KEY,
        Title TEXT NOT NULL,
        ReleaseYear INTEGER CHECK (ReleaseYear >= 1799),
        AgeRatingID INTEGER NOT NULL,
        Runtime INTEGER CHECK (Runtime >= 0),
        GenreID INTEGER,
        FOREIGN KEY (AgeRatingID) REFERENCES AgeRatings (AgeRatingID),
        FOREIGN KEY (GenreID) REFERENCES Genres (GenreID)
    );''')

    return True


def create_users(conn):
    '''Create users table and lookup tables'''

    conn.execute('''CREATE TABLE IF NOT EXISTS Users (
        ID INTEGER PRIMARY KEY,
        Username TEXT NOT NULL CHECK (LENGTH(Username) >= 3 AND LENGTH(Username) <= 25),
        Password TEXT NOT NULL,
        CONSTRAINT CheckPassLength CHECK (LENGTH(Password) >= 12 AND LENGTH(Password) <= 255),
        CONSTRAINT CheckPassChars CHECK (Password LIKE '%[0-9]%' AND Password LIKE '%[A-Z]%' \
        AND Password LIKE '%[a-z]%' AND Password LIKE '%[!@#$%a^&*()-_+=.,;:''"`~]%')
    );''')

    return True;

# If this program is run in terminal, execute its function.
if __name__ == '__main__':
    conn = sqlite3.connect('silverscreen.db')
    print('Connected to database')

    if create(conn):
        print('Created movies table and lookup tables')
    else:
        print('Error creating movies table')
    if create_users(conn):
        print('Created users table')
    else:
        print('Error creating users table')
    print('Operation completed successfully')
