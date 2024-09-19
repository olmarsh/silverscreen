'''Create the silverscreen database, add movie/user table and lookup tables.'''

import sqlite3

def create(conn):
    '''Create silverscreen movie table and lookup tables.'''

    # Enable foreign keys
    conn.execute('PRAGMA foreign_keys = ON;')

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

    # Create ratings and favourite tables
    conn.execute('''CREATE TABLE IF NOT EXISTS Ratings (
        RatingID INTEGER PRIMARY KEY,
        MovieID INTEGER NOT NULL,
        UserID INTEGER NOT NULL,
        Rating REAL NOT NULL CHECK (Rating >= 0 AND Rating <= 5),
        FOREIGN KEY (MovieID) REFERENCES Movies(ID) ON DELETE CASCADE,
        FOREIGN KEY (UserID) REFERENCES Users(ID) ON DELETE CASCADE,
        UNIQUE (UserID, MovieID)
    );''')
    conn.execute('''CREATE TABLE IF NOT EXISTS Favourites (
        FavouriteID INTEGER PRIMARY KEY,
        MovieID INTEGER NOT NULL,
        UserID INTEGER NOT NULL,
        FOREIGN KEY (MovieID) REFERENCES Movies(ID) ON DELETE CASCADE,
        FOREIGN KEY (UserID) REFERENCES Users(ID) ON DELETE CASCADE,
        UNIQUE (UserID, MovieID)
    );''')

    return True


def create_users(conn):
    '''Create users table and lookup tables'''

    conn.execute('''CREATE TABLE IF NOT EXISTS Users (
        ID INTEGER PRIMARY KEY,
        Username TEXT UNIQUE NOT NULL CHECK (LENGTH(Username) >= 3 AND LENGTH(Username) <= 25),
        Password TEXT NOT NULL,
        Admin INTEGER NOT NULL DEFAULT 0
    );''')

    return True;

# If this program is run in terminal, execute its function.
if __name__ == '__main__':
    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    print('Connected to database')

    if create_users(conn):
        print('Created users table')
    else:
        print('Error creating users table')

    if create(conn):
        print('Created movies table and lookup tables')
    else:
        print('Error creating movies table')
    print('Operation completed successfully')
