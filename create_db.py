import sqlite3

conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

# Create movies table
conn.execute('''CREATE TABLE Movies (
    ID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    ReleaseYear INTEGER CHECK (ReleaseYear >= 1799),
    AgeRating TEXT NOT NULL,
    Runtime INTEGER CHECK (Runtime >= 0),
    Genre TEXT
);''')

# Create genre lookup table
conn.execute('''CREATE TABLE Genres (
GenreID INTEGER PRIMARY KEY,
Name TEXT,
Symbol TEXT,
FOREIGN KEY (GenreID) REFERENCES Genres (GenreID));''')

# Create age rating lookup table
conn.execute('''CREATE TABLE AgeRatings (
AgeRatingID INTEGER PRIMARY KEY,
Name TEXT,
MinAge INTEGER,
FOREIGN KEY (AgeRatingID) REFERENCES Genres (AgeRatingID));''')

print('Table created successfully')
