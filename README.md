# silverscreen: Movie Database
<p align='center'>
<img src='./static/logo.svg' width=100px>
</p>

silverscreen is a movie database which stores information about movies. Not only that, it also functions as a web server and can store user information, with a favourites and ratings system. (Computer Science project for CS Level 2 2024)

### Built in
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

### License
silverscreen is licensed under the MIT License.

## Getting Started
### Clone the repository
Clone this repository via `git clone https://github.com/olmarsh/silverscreen` or download and extract the zip.
### Set up the database
#### Install necessary modules
This project requires the modules:
* Flask
* Flask-SocketIO
* Flask-Login
* Bcrypt

These can be installed via the following command:
```pip install flask flask-socketio bcrypt flask-login```
The project was written and tested in Python 3.12 with the latest versions of all modules.

#### Try out functionality
To experiment with the program, you can make a copy of the `silverscreen_example.db` file named `silverscreen.db` before first running the program. Then, go to the instructions for {}
#### Set up a new database
Alternatively, you might want to start a new database from scratch. To do this, ensure there are no files named `silverscreen.db`, then run `ss_cli.py` from a terminal emulator from the root directory.

```python ss_cli```

Then, run the following commands from the cli:
* `CREATE` - create the necessary tables for the database
* `PPLATE` - populate the lookup tables with the default values

Congratulations! Your silverscreen database is now functional.
### Fill the database
To help fill out your new database, you can import the default list of 33 films from the cli: `IMPORT`

You will be given the choice of whether to preserve movie IDs. If your database already contains entries, choose `N`, else choose `Y`.
### Create an admin user
You will also want to create an admin user so you can manage the database from the web interface. This can also be done through the cli.

_To create the user_
Choose `INSERT`, then choose `Users`, and enter the username and password for your new user. This user is then added to the database.

_To give it administrator_
Choose `UPDATE`, then choose `Users`. Enter the ID of your user (it should be `1` if it is the first user), and finally `Admin`. Then, type `y` to give the user admin perms.
### Run the server!
Now your database is set up, you can `EXIT` the cli and run `ss_flask.py` from the root directory. This will open a web server on `localhost:5000` or `127.0.0.1:5000`. After this, open your web browser of choice and navigate to one of those pages.

From here, you can navigate to the different parts of the web app from the top bar. You can view the movies page, sign into different accounts, leave ratings and favourites and more!

To access web management tools, log into an account which has been granted administrator by the command line interface.

## Notes about deployment
Before deploying the app to a production server, ensure to change the secret key on line 14 of `ss_flask.py`. Depending on your environment, you will also want to change the host IP on line 15 of the same file.

Good luck!
