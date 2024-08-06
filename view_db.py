'''Print the entire movies database'''

import sqlite3

conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

for row in conn.execute('''SELECT * FROM Movies
INNER JOIN Genres ON Movies.GenreID = Genres.GenreID
INNER JOIN AgeRatings on Movies.AgeRatingID = AgeRatings.AgeRatingID
ORDER BY ID ASC'''):
#    (
#        ID,
#        Title,
#        ReleaseYear,
#        AgeRating,
#        Runtime,
#        Genre,
#    ) = row
    print(row)

print('Operation done successfully')
