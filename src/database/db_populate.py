'''Add the default values to the tables'''

import sqlite3

conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

# Populate genres table
conn.execute('''INSERT INTO Genres (Genre, Symbol)
VALUES
('Action','💣'),
('Animation', '🎞️'),
('Comedy', '😂'),
('Crime', '🔍'),
('Fantasy', '🪄')
''')

# Populate age ratings table
conn.execute('''INSERT INTO AgeRatings (AgeRating, MinAge, Description)
VALUES
('G', 0, 'General Audiences'),
('PG', 0, 'Parental Guidance Suggested'),
('PG-13', 13, 'Parents Strongly Cautioned'),
('R', 17, 'Restricted'),
('NC-17', 17, 'Adults Only')
''')

conn.commit()

print('Populated tables with default values')
