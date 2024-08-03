import sqlite3

# Connect to database
conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

# Get user inputs for new movie
print('Add new movie to database')
title = input('Movie title:  ')
releaseYear = int(input('Release year: '))
ageRating = input('Age rating:   ')
runtime = int(input('Runtime:      '))
genre = input('Genre:        ')

conn.execute(f'''INSERT INTO Movies (
    Title, ReleaseYear, AgeRating, Runtime, Genre
)
VALUES (
    '{title}',
    '{releaseYear}',
    '{ageRating}',
    '{runtime}',
    '{genre}'
);''')

conn.commit()

print('Operation done successfully')
