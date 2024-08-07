'''Add an entry to a silverscreen database'''

import sqlite3

# Connect to database
conn = sqlite3.connect('silverscreen.db')
cursor = conn.cursor()
print('Connected to database')

# Get user inputs for new movie
print('Add new movie to database')
title = input('Movie title:  ')
releaseYear = int(input('Release year: '))
ageRating = input('Age rating:   ')
runtime = int(input('Runtime:      '))
genre = input('Genre:        ')

# Get genre ID
cursor.execute(f'SELECT * FROM Genres WHERE Genre = \'{genre}\'')
genreID = cursor.fetchone()[0]
print(f'Read genre id: {genreID}')

# Get AgeRating ID
cursor.execute(f'SELECT * FROM AgeRatings WHERE AgeRating = \'{ageRating}\'')
ageRatingID = cursor.fetchone()[0]
print(f'Read age rating id: {ageRatingID}')

conn.execute(f'''INSERT INTO Movies (
    Title, ReleaseYear, AgeRatingID, Runtime, GenreID
)
VALUES (
    '{title}',
    '{releaseYear}',
    '{ageRatingID}',
    '{runtime}',
    '{genreID}'
);''')

conn.commit()

print('Operation done successfully')
