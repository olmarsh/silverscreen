'''Print all tables from the database.'''

import sqlite3

conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

for row in conn.execute('''SELECT * FROM Movies
INNER JOIN Genres ON Movies.GenreID = Genres.GenreID
INNER JOIN AgeRatings on Movies.AgeRatingID = AgeRatings.AgeRatingID
ORDER BY ID ASC'''):
    print(row)

print('Operation done successfully')
