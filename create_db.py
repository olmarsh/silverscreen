import sqlite3

conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

# Create genre lookup table
conn.execute('''CREATE TABLE Genres (
GenreID INTEGER PRIMARY KEY,
Name TEXT,
Symbol TEXT
);''')

# Create age rating lookup table
conn.execute('''CREATE TABLE AgeRatings (
AgeRatingID INTEGER PRIMARY KEY,
Name TEXT,
MinAge INTEGER,
Description TEXT,
FOREIGN KEY (AgeRatingID) REFERENCES Genres (AgeRatingID)
);''')

# Populate genres table
conn.execute('''INSERT INTO Genres (Name, Symbol)
VALUES
('Action','💣'),
('Animation', '🎞️'),
('Comedy', '😂'),
('Crime', '🔍'),
('Fantasy', '🪄');
''')

# Populate age ratings table
conn.execute('''INSERT INTO AgeRatings (Name, MinAge, Description)
VALUES
('G', 0, 'General Audiences'),
('PG', 0, 'Parental Guidance Suggested'),
('PG-13', 13, 'Parents Strongly Cautioned'),
('R', 17, 'Restricted'),
('NC-17', 17, 'Adults Only');
''')

# Create movies table
conn.execute('''CREATE TABLE Movies (
    ID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    ReleaseYear INTEGER CHECK (ReleaseYear >= 1799),
    AgeRatingID INTEGER NOT NULL,
    Runtime INTEGER CHECK (Runtime >= 0),
    GenreID INTEGER,
    FOREIGN KEY (AgeRatingID) REFERENCES AgeRatings (AgeRatingID),
    FOREIGN KEY (GenreID) REFERENCES Genres (GenreID)
);''')

print('Tables created successfully')
