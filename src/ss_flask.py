from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import database
import sqlite3

import database.db_delete
import database.db_insert
import database.db_update
import database.db_view

# Flask setup
app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*')

# Page definitions

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/movie')
def movie():
    # Get the movie id from the URL parameter
    id = request.args.get('id')

    # Check if the user wants to edit the movie
    edit = request.args.get('edit')
    if edit == 'true': edit = True
    
    # If the user wants only to view
    if not edit:
        # Open a connection to the database and view movie
        conn = sqlite3.connect('silverscreen.db')
        try:
            movie = database.db_view.search_movies(conn, 'ID', id, limit=1)[0]
            return render_template('movie.html',
                                title=movie[1],
                                releaseyear=movie[2],
                                runtime=str(movie[3])+' minutes',
                                genre=movie[4]+' '+movie[6],
                                agerating=movie[5]+' ('+movie[8]+')',
                                id=movie[0])
        except:  # If the id was invalid, return the error template
            return render_template('error.html')
        
    else:  # If the user wants to edit, return the edit template
                # Open a connection to the database and view movie
        conn = sqlite3.connect('silverscreen.db')
        movie = database.db_view.search_movies(conn, 'ID', id, limit=1)[0]
        genre_options = format_options('Genres')
        return render_template('edit.html', action='edit', heading='Editing',
                    title=movie[1],
                    releaseyear=movie[2],
                    runtime=movie[3],
                    genre=movie[4],
                    agerating=movie[5],
                    id=movie[0],
                    genre_options=genre_options,
                    agerating_options=format_options('AgeRatings'))

@app.route('/add')
def add():
    return render_template('add.html',
                    genre_options=format_options('Genres'),
                    agerating_options=format_options('AgeRatings'))

@app.route('/delete')
def delete():
    id = request.args.get('id')
    conn = sqlite3.connect('silverscreen.db')
    try:
        movie = database.db_view.search_movies(conn, 'ID', id, limit=1)[0]
        return render_template('delete.html',
                        title=movie[1],
                        releaseyear=movie[2],
                        runtime=str(movie[3])+' minutes',
                        genre=movie[4]+' '+movie[6],
                        agerating=movie[5]+' ('+movie[8]+')',
                        id=movie[0]
                        )
    except:  # If the id was invalid, return the error template
        return render_template('error.html')

# Handle a request to delete a movie
@app.route('/handle_delete', methods=['POST'])
def handle_delete():
    id = request.form['id']
    conn = sqlite3.connect('silverscreen.db')
    try:
        if database.db_delete.delete(conn, 'Movies', 'ID', id):
            conn.commit()
            return f'Success<br><a href="/movies"> \
                    Return to table view</a>'
        return f'Failure (invalid)<br><a href="javascript:history.back()"> \
                Return to delete page</a>'
    except:
        return f'Failure (invalid)<br><a href="javascript:history.back()"> \
                Return to delete page</a>'


# Handle when a request to edit or add movie to the database is sent
@app.route('/handle_edit', methods=['POST'])
def handle_edit():
    print(request.form)
    # Get form values
    title = request.form['title']
    release_year = request.form['releaseyear']
    runtime = request.form['runtime']
    genre = request.form['genre']
    age_rating = request.form['agerating']

    # If the user wants to edit
    if request.form['action'] == 'edit':
        movie_id = request.form['id']
        # Connect to the table and update the values according to the form
        try:
            conn = sqlite3.connect('silverscreen.db')
            if database.db_update.update(conn, movie_id, {
                'Title': title,
                'ReleaseYear': release_year,
                'Runtime': runtime,
                'Genre': genre,
                'AgeRating': age_rating
            }):
                conn.commit()
                return f'Success<br><a href="/movie?id={movie_id}"> \
                        Return to movie page</a>'
            return f'Failure (invalid)<br><a href="javascript:history.back()"> \
                    Return to edit page</a>'

        except Exception as error:
            conn.close()
            return f'Failure ({type(error).__name__+'\n'+str(error)})<br> \
                    <a href="javascript:history.back()"> \
                    Return to edit page</a>'
        
    # If the user wants to add a new movie
    elif request.form['action'] == 'insert':
# Connect to the table and update the values according to the form
        try:
            conn = sqlite3.connect('silverscreen.db')
            if database.db_insert.insert(conn, "Movies",
                title = title,
                releaseYear = release_year,
                runtime = runtime,
                genre = genre,
                ageRating = age_rating
            ):
                conn.commit()

                # Get most recent row added
                cursor = conn.cursor()
                cursor.execute('SELECT last_insert_rowid()')
                movie_id = cursor.fetchone()[0]

                return f'Success<br><a href="/movie?id={movie_id}"> \
                        Go to new movie page</a>'
            return f'Failure (invalid)<br><a href="javascript:history.back()"> \
                    Return to add movie page</a>'

        except Exception as error:
            conn.close()
            return f'Failure ({type(error).__name__+'\n'+str(error)})<br> \
                    <a href="javascript:history.back()"> \
                    Return to add movie page</a>'


# Confirm to client that connection was successful
@socketio.on('connect')
def test_connect():
    emit('connected',  {'data':'Connected'})  # Confirm the client connected

@socketio.on('')

# When a table is requested:
@socketio.on('table_request')
def update_table(results_per_page, read_page, read_order, read_search='',
                 read_search_type='', datetime=0):
    # Sanitise page information
    try:
        limit = int(results_per_page)
    except:
        limit = 20
    if limit == 0: limit = 20

    try:
        page = int(read_page)
    except:
        page = 1
    if page < 1: page = 1

    # If there was a query, read its search type and escape its characters
    match_before = True
    if read_search != '':
        search = escape_query(read_search)
        if read_search_type == 'Title':
            search_type = 'Title'
            match_before = True
        elif read_search_type == 'Release Year':
            search_type = 'ReleaseYear'
            match_before = False
        elif read_search_type == 'Runtime':
            search_type = 'Runtime'
            match_before = False
        elif read_search_type == 'Genre':
            search_type = 'Genre'
            match_before = True
        elif read_search_type == 'Age Rating':
            search_type = 'AgeRating'
            match_before = False

        
    # Set order for query based on request
    if read_order == 'title-asc': order = 'Title ASC'
    elif read_order == 'title-desc': order = 'Title DESC'
    elif read_order == 'releaseyear-desc': order = 'ReleaseYear DESC'
    elif read_order == 'releaseyear-asc': order = 'ReleaseYear ASC'
    elif read_order == 'runtime-asc': order = 'Runtime ASC'
    elif read_order == 'runtime-desc': order = 'Runtime DESC'
    elif read_order == 'genre-asc': order = 'Genre ASC'
    elif read_order == 'genre-desc': order = 'Genre DESC'

    # Connect to database and request rows
    conn = sqlite3.connect('silverscreen.db')

    if read_search == '':  # If nothing was searched, request the entire db
        movies = database.db_view.view_movies(conn, limit=limit,
                                              offset=(page-1)*limit,
                                              order=order)
        results_count = database.db_view.count_movies(conn)
    else: 
        movies = database.db_view.search_movies(conn, search_type, search,
                                                limit=limit,
                                                offset=(page-1)*limit,
                                                order=order,
                                                match_before=match_before)
        results_count = database.db_view.count_movies(conn, search_type,
                                                      search, match_before=\
                                                      match_before)

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

    emit('table_update', {
            'table_content': content,
            'result_count': results_count,
            'page': page,
            'datetime': datetime
        })

# Function definitions


def format_table_row(row):
    '''Format a row of the movies table to be displayed.'''

    return f'''<tr><td><a href='/movie?id={row[0]}'>{row[1]}</a></td>
    <td>{row[2]}</td>
    <td>{row[3]}</td>
    <td>{row[4]}</td>
    <td>{row[5]}</td>
    <td><a href='/delete?id={row[0]}'>❌</a></tr>'''

def format_options(table):
    '''Format genre or age rating options for a dropdown'''

    conn = sqlite3.connect('silverscreen.db')
    results = database.db_view.view_general(conn, table)

    # Create an empty string, then fill it with all the names, and return
    ret = ''
    for i in results:
        ret += '<option>' + str(i[1]) + '</option>'

    return ret


def escape_query(inp):
    '''Escape all double and single quotes to prevent SQL injection'''

    ret = inp
    ret = ret.replace('\'', '\'\'')
    ret = ret.replace('"', '""')

    return ret

if __name__ == '__main__':
   app.run()
