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
    # TODO: return results via a websocket
    # and only return the first 20 at once anyway

    conn = sqlite3.connect('silverscreen.db')
    movies = database.db_view.view_movies(conn)

    # Format each row and add it to the table content
    content = ''
    for row in movies:
        content += format_table_row(row) + '\n'

    content += '</table>'

    # Return the movies page with the table content
    return render_template('movies.html', table_content=content)


# Test connection to client
@socketio.on("connect")
def test_connect():
    emit("connected",  {"data":"Connected"})  # Confirm the client connected


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