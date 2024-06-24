import sqlite3

conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

conn.execute('''CREATE TABLE Movies (
    ID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    ReleaseYear INTEGER,
    AgeRating TEXT NOT NULL,
    Runtime INTEGER,
    Genre TEXT
);''')
         
print('Table created successfully')
