from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3

import database
import database.db_delete
import database.db_insert
import database.db_update
import database.db_view

# Flask setup
app = Flask(__name__)
app.secret_key = 'development'
host = '127.0.0.1'
socketio = SocketIO(app,cors_allowed_origins='*')

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):    
    return User(user_id)

class User():
    # Initialise user with ID
    def __init__(self, user_id):
        conn = sqlite3.connect('silverscreen.db')
        conn.execute('PRAGMA foreign_keys = ON;')
        user_info = database.db_view.search_users(
                    conn, 'ID', user_id, limit=1, match_before=False,
                    match_after = False
                )[0]
        self.user_id = user_id
        self.username = user_info[1]
        self.admin = user_info[3]
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False

    def get_id(self):
        return self.user_id
    

# Allow caching of the logo to prevent flickering
@app.route('/static/logo.svg')
def logo_static():
    response = send_from_directory('static', 'logo.svg')
    response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    return response

# Page definitions

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movies')
def movies():
    popup = request.args.get('popup')
    # If there is no popup message, do not show popup
    if popup == '' or popup == None:
        return render_template('movies.html')
    # Else show popup message and make it visible.
    return render_template('movies.html', popup_visible='display', popup_message=popup)

@app.route('/movie')
def movie():
    # Get the popup text from url parameters
    popup = request.args.get('popup')
    # If there is no popup message, do not show popup
    if popup == '' or popup == None:
        popup_display = ''
    else:
        popup_display = 'display'

    # Get the movie id from the URL parameter
    id = request.args.get('id')

    # Check if the user wants to edit the movie
    edit = request.args.get('edit')
    if edit == 'true': edit = True
    
    # If the user wants only to view
    if not edit:
        # Open a connection to the database and view movie
        conn = sqlite3.connect('silverscreen.db')
        conn.execute('PRAGMA foreign_keys = ON;')
        try:
            movie = database.db_view.search_movies(conn, 'ID', id, limit=1,
                                                   match_before=False,
                                                   match_after=False,
                                                   user=current_user.get_id())[0]
            return render_template('movie.html',
                                title=movie[1],
                                releaseyear=movie[2],
                                runtime=str(movie[3])+' minutes',
                                genre=movie[4],
                                genre_symbol=movie[6],
                                agerating=movie[5],
                                agerating_description=movie[8],
                                id=movie[0],
                                rating=(movie[9] if movie[9] is not None else 0),
                                user_rating=(movie[13] if movie[13] is not None else 0),
                                rating_count=movie[10],
                                favourite_visible=('visible' if movie[12] == 1 else 'hidden'),
                                favourite_count=movie[11],
                                popup_visible=popup_display, popup_message=popup)
        except:  # If the id was invalid, return the error template
            return render_template('error.html', error_statement='404 Not Found'), 404
        
    else:  # If the user wants to edit, return the edit template
        # Do not process request if user is not admin
        if current_user.get_id() == None or current_user.admin == 0:
            return render_template('error.html', error_statement='403 Forbidden (Not admin)'), 403
    
        # Open a connection to the database and view movie
        conn = sqlite3.connect('silverscreen.db')
        conn.execute('PRAGMA foreign_keys = ON;')

        movie = database.db_view.search_movies(conn, 'ID', id, limit=1,
                                               match_before=False,
                                               match_after=False)[0]
        return render_template('edit.html', action='edit', heading='Editing',
                    title=movie[1],
                    releaseyear=movie[2],
                    runtime=movie[3],
                    id=movie[0],
                    genre_options=format_options('Genres', movie[4]),
                    agerating_options=format_options('AgeRatings', movie[5]))

@app.route('/send_favourite/', methods=['POST'])
def handle_favourite():
    movie_id = request.form['movie_id']
    conn = sqlite3.connect('silverscreen.db')

    # If the user isn't logged in, send them to the login page
    if current_user.get_id() == None:
        return '1'
    
    conn.execute('PRAGMA foreign_keys = ON;')

    # See if a favourite already exists
    existing = database.db_view.search_favourites_ratings(conn, 'Favourites',
                                               user_id=current_user.get_id(),
                                               movie_id=movie_id)
    
    # If there was no favourite, insert one
    if existing == []:
        database.db_insert.favourite_insert(conn, current_user.get_id(), movie_id)
        conn.commit()
    # If there was a favourite, remove it.
    else:
        database.db_delete.delete(conn, 'Favourites',
                                  match_column='FavouriteID',
                                  delete_id=existing[0][0])
        conn.commit()

    return '0'

@app.route('/send_rating/', methods=['POST'])
def handle_rating():
    movie_id = request.form['movie_id']
    rating = request.form['rating']

    # If the user isn't logged in, send them to the login page
    if current_user.get_id() == None:
        return '1'

    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')

    # See if a rating already exists
    existing = database.db_view.search_favourites_ratings(conn, 'Ratings',
                                               user_id=current_user.get_id(),
                                               movie_id=movie_id)
    
    print(movie_id)

    # If there was no rating, insert one
    if existing == []:
        database.db_insert.rating_insert(conn, current_user.get_id(),
                                         movie_id=movie_id,
                                         rating=rating)
        conn.commit()
    # If there was a rating, edit it, or delete.
    else:
        if rating == '0':
            database.db_delete.delete(conn, 'Ratings', 'RatingID', existing[0][0])
        else:
            database.db_update.update_rating(conn, user_id=current_user.get_id(),
                                            movie_id=movie_id, 
                                            value=rating)
        conn.commit()

    print('Rating', movie_id, rating)
    return '0'

@app.route('/add')
def add():
    # Do not process request if user is not admin
    if current_user.get_id() == None or current_user.admin == 0:
        return render_template('error.html', error_statement='403 Forbidden (Not admin)'), 403
    
    return render_template('add.html',
                    genre_options=format_options('Genres'),
                    agerating_options=format_options('AgeRatings'))

@app.route('/delete')
def delete():
    # Do not process request if user is not admin
    if current_user.get_id() == None or current_user.admin == 0:
        return render_template('error.html', error_statement='403 Forbidden (Not admin)'), 403
    
    id = request.args.get('id')
    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    try:
        movie = database.db_view.search_movies(conn, 'ID', id, limit=1)[0]
        return render_template('delete.html',
                        title=movie[1],
                        releaseyear=movie[2],
                        runtime=str(movie[3])+' minutes',
                        genre=movie[4],
                        genre_symbol=movie[6],
                        agerating=movie[5],
                        agerating_description=movie[8],
                        id=movie[0]
                        )
    except:  # If the id was invalid, return the error template
        return render_template('error.html', error_statement='404 Not Found'), 404

# Handle a request to delete a movie
@app.route('/handle_delete', methods=['POST'])
def handle_delete():
    # Do not process request if user is not admin
    if current_user.get_id() == None or current_user.admin == 0:
        return render_template('error.html', error_statement='403 Forbidden (Not admin)'), 403
    
    id = request.form['id']
    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    try:
        if database.db_delete.delete(conn, 'Movies', 'ID', id):
            conn.commit()
            # Return the movie table page
            return redirect(url_for('movies', popup="Deleted successfully", popup_visible='display'))
        return render_template('error.html', error_statement='Failure (invalid)',
                               return_statement='Return to delete page')
    except Exception as error:
        return render_template('error.html', error_statement=f'Failure ({type(error).__name__+'\n'+str(error)})',
                               return_statement='Return to delete page')

# Handle when a request to edit or add movie to the database is sent
@app.route('/handle_edit', methods=['POST'])
def handle_edit():
    # Do not process request if user is not admin
    if current_user.get_id() == None or current_user.admin == 0:
        return render_template('error.html', error_statement='403 Forbidden (Not admin)'), 403
    
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
            conn.execute('PRAGMA foreign_keys = ON;')
            if database.db_update.update(conn, movie_id, {
                'Title': title,
                'ReleaseYear': release_year,
                'Runtime': runtime,
                'Genre': genre,
                'AgeRating': age_rating
            }):
                conn.commit()
                return redirect(url_for('movie', id=movie_id, popup="Edited movie successfully"))
            return render_template('error.html', error_statement='Failure (invalid)',
                                    return_statement='Return to edit page')

        except Exception as error:
            conn.close()
            return render_template('error.html', error_statement=f'Failure ({type(error).__name__+'\n'+str(error)})',
                                    return_statement='Return to edit page')
        
    # If the user wants to add a new movie
    elif request.form['action'] == 'insert':
# Connect to the table and update the values according to the form
        try:
            conn = sqlite3.connect('silverscreen.db')
            conn.execute('PRAGMA foreign_keys = ON;')
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

                return redirect(url_for('movie', id=movie_id, popup="Added movie successfully"))
            return render_template('error.html', error_statement=f'Failure (Invalid)',
                                    return_statement='Return to add movie page')
        except Exception as error:
            conn.close()
            return render_template('error.html', error_statement=f'Failure ({type(error).__name__+'\n'+str(error)})',
                                    return_statement='Return to add movie page')

# Login and signup
@app.route('/login')
def login():
    # Get the popup text from url parameters
    popup = request.args.get('popup')
    # If there is no popup message, do not show popup
    if popup == '' or popup == None:
        popup_display = ''
    else:
        popup_display = 'display'
    return render_template('login.html', popup_visible=popup_display, popup_message=popup)

@app.route('/handle_login', methods=['POST'])
def handle_login():
    # Get username and password from form
    username = escape_query(request.form['username'])
    password = escape_query(request.form['password'])
    
    # Authenticate against hash in database
    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    try:
        if database.db_login.authenticate(conn, username, password):
            # Get the ID of this user if password was correct
            login_user(User(database.db_view.search_users(
                conn, 'username', username, limit=1, match_before=False,
                match_after = False
                )[0][0]))
            return redirect('/movies')
        else:
            return redirect(url_for('login', popup='Username or password incorrect'))
    except:
        return redirect(url_for('login', popup='Username or password incorrect'))
    
@app.route('/signup')
def signup():
    # Get the popup text from url parameters
    popup = request.args.get('popup')
    # If there is no popup message, do not show popup
    if popup == '' or popup == None:
        popup_display = ''
    else:
        popup_display = 'display'
    
    return render_template('signup.html', popup_visible=popup_display, popup_message=popup)

@app.route('/handle_signup', methods=['POST'])
def handle_signup():
    # Get username and password from form
    username = escape_query(request.form['username'])
    password = escape_query(request.form['password'])
    
    # Authenticate against hash in database
    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    try:
        if database.db_insert.user_insert(conn, username, password):
            conn.commit()
            return redirect(url_for('login', popup='Signed up successfully'))
        else:
            return redirect(url_for('signup', popup='Failure'))
    except Exception as error:
        return redirect(url_for('signup', popup=f'Failure: {error}'))

@app.route("/logout")
@login_required
def logout():
    redirect_page = request.args.get('redirect')
    logout_user()
    return redirect(f'/{redirect_page}')


# Confirm to client that connection was successful
@socketio.on('connect')
def test_connect():
    emit('connected',  {'data':'Connected'})  # Confirm the client connected

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
    elif read_order == 'rating-desc': order = 'Rating DESC'
    elif read_order == 'favourites-desc': order = 'TotalFavourites DESC'
    elif read_order == 'user-favourites': order = 'IsFavourite DESC'

    # Connect to database and request rows
    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')

    if read_search == '':  # If nothing was searched, request the entire db
        results_count = database.db_view.count_movies(conn)

        # Limit page number to number of results
        if page > (results_count // int(results_per_page))+1:
            page = (results_count // int(results_per_page))+1

        movies = database.db_view.view_movies(conn, limit=limit,
                                              offset=(page-1)*limit,
                                              order=order,
                                              user=current_user.get_id())
    else:
        results_count = database.db_view.count_movies(conn, search_type,
                                                      search, match_before=\
                                                      match_before)
        # Limit page number to number of results
        if page > (results_count // int(results_per_page))+1:
            page = (results_count // int(results_per_page))+1

        movies = database.db_view.search_movies(conn, search_type, search,
                                                limit=limit,
                                                offset=(page-1)*limit,
                                                order=order,
                                                match_before=match_before,
                                                user = current_user.get_id())

    # Create table headers
    content = f'''
    <tr class="movies-table-headers">
        <th class="movies-table-title">Title</th>
        <th>Release Year</th>
        <th>Runtime (min)</th>
        <th class="movies-table-genre">Genre</th>
        <th>Age Rating</th>
        <th></th><th></th>{'<th></th>'
                           if current_user.is_authenticated
                           and current_user.admin == 1
                           else ''
                           }
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
    <td>{row[6]} {row[4]}</td>
    <td>{row[5]}</td>
    <td><div class="favourite-movie-button" onclick="send_favourite('{row[0]}')"
    style="--visibility:
        {'visible' if row[12] == 1 else 'hidden'};"> ({row[11]})
    </div></td>
    <td><div class="ratings-row"><div class="ratings-display" style="--rating:
        {row[9] if row[9] is not None else 0}"></div><span style="align-self: flex-end">
        ({row[10]})</span>
    </div></td>
    {'<td><a href=\'/delete?id={row[0]}\' class="delete-movie-button">❌</a></td>'
    if current_user.is_authenticated
    and current_user.admin == 1
    else ''
    }</tr>'''

def format_options(table, selected=None):
    '''Format genre or age rating options for a dropdown'''

    conn = sqlite3.connect('silverscreen.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    results = database.db_view.view_general(conn, table)

    # Create an empty string, then fill it with all the names, and return
    ret = ''
    for i in results:
        # If this option is the selected value, select its option
        if selected == str(i[1]):
            ret += '<option selected>' + str(i[1]) + '</option>'
        else:
            ret += '<option>' + str(i[1]) + '</option>'

    return ret


def escape_query(inp):
    '''Escape all double and single quotes to prevent SQL injection'''

    ret = inp
    ret = ret.replace('\'', '\'\'')
    ret = ret.replace('"', '""')

    return ret

if __name__ == '__main__':
   app.run(host=host)
