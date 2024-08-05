import sqlite3

# Connect to database
conn = sqlite3.connect('silverscreen.db')
cursor = conn.cursor()
print('Connected to database')

edit_id = int(input('Which movie ID to edit: '))
print(f'Editing movie ID {edit_id}')

field = input('Which field to change: ')
print(f'Editing field {field}')

value = input('What value to set the field to: ')
print(f'Setting {field} to {value}')

# If the field was genre or age rating, do the
# appropriate action with the lookup table.
if (field == 'Genre'):
    cursor.execute(f'SELECT * FROM Genres WHERE Genre = \'{value}\'')
    field = 'GenreID'
    value = cursor.fetchone()[0]
    print(f'Read genre id: {value}')

if (field == 'AgeRating'):
    cursor.execute(f'SELECT * FROM AgeRatings WHERE AgeRating = \'{value}\'')
    field = 'AgeRatingID'
    value = cursor.fetchone()[0]
    print(f'Read age rating id: {value}')

conn.execute(f'''UPDATE Movies SET
{field} = '{value}'
WHERE ID = {edit_id};
''')

print('Table updated successfully')

conn.commit()
