from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import database
import sqlite3

# Flask setup
app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*')

# Page definitions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movies')
def movies():
    # Return the movies page with the table content
    return render_template('movies.html')


# Confirm to client that connection was successfull
@socketio.on('connect')
def test_connect():
    emit('connected',  {'data':'Connected'})  # Confirm the client connected

@socketio.on('')

# When a table is requested:
@socketio.on('table_request')
def update_table():
    # TODO: Only return the first 20 results at once

    conn = sqlite3.connect('silverscreen.db')
    movies = database.db_view.view_movies(conn)

    # Create table headers
    content = '''
<tr>
    <th>Title</th>
    <th>Release Year</th>
    <th>Runtime (min)</th>
    <th>Genre</th>
    <th>Age Rating</th>
</tr>
'''
    # Format each row and add it to the table content
    for row in movies:
        content += format_table_row(row) + '\n'

    emit('table_update', content)

# Function definitions


def format_table_row(row):
    '''Format a row of the movies table to be displayed.'''

    return f'''<tr><td>{row[1]}</td>
    <td>{row[2]}</td>
    <td>{row[3]}</td>
    <td>{row[4]}</td>
    <td>{row[5]}</td></tr>'''


if __name__ == '__main__':
   app.run()