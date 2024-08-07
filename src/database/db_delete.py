'''Delete an entry from a database.'''

import sqlite3

conn = sqlite3.connect("silverscreen.db")
print("Connected to database")

delete_id = input('Which movie ID to delete: ')

conn.execute(f'''DELETE FROM Movies
WHERE ID = {delete_id};
''');

print('Deleted entry successfully')

conn.commit();
