import sqlite3

# Connect to database
conn = sqlite3.connect('silverscreen.db')
print('Connected to database')

edit_id = int(input('Which movie ID to edit: '))
print(f'Editing movie ID {edit_id}')

field = input('Which field to change: ')
print(f'Editing field {field}')

value = input('What value to set the field to: ')
print(f'Setting {field} to {value}')

conn.execute(f'''UPDATE Movies SET
{field} = '{value}'
WHERE ID = {edit_id};
''')

print('Table updated successfully')

conn.commit()
