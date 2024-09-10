'''Log a user into their account via username and password.'''

import sqlite3
import bcrypt

def authenticate(conn, username, password):
    '''Authenticate the user's details'''

    cursor = conn.cursor()

    # Get username and password
    cursor.execute(f'''SELECT * FROM Users WHERE username = '{username}' ''')
    user_details = cursor.fetchone()

    username = user_details[1];
    hash = user_details[2];
    
    if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hash, 'utf-8')):
        return True, user_details
    else: return False

if __name__ == '__main__':
    username = input('Username: ')
    password = input('Password: ')

    conn = sqlite3.connect('silverscreen.db')
    
    user = authenticate(conn, username, password)

    # If the hash of the password matched the stored hash, authenticate the user.
    if user:
        print('Login Successful')
        print(user[1])
    else:
        print('Login Unsuccessful')