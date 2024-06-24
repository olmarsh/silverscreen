import sqlite3

conn = sqlite3.connect("silverscreen.db")
print("Connected to database")

for row in conn.execute("SELECT * FROM Movies ORDER BY ID ASC"):
    (
        ID,
        Title,
        ReleaseYear,
        AgeRating,
        Runtime,
        Genre,
    ) = row
    print(row)

print("Operation done successfully")
