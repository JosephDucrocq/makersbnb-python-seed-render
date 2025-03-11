import os

from lib.user_repository import *
from lib.space_repository import *
from flask import Flask, request, render_template, session, redirect
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.user import User

# Create a new Flask app
app = Flask(__name__)
app.secret_key = 'this_is_a_super_secret_key'

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index

@app.route('/', methods=["GET"])
def welcome():
    if session['username'] != None:
        username = f"Logged in as: {session['username']}"
        _connection = get_flask_database_connection(app)
        users_repository = UserRepository(_connection)
        user_id = users_repository.find_by_username(session['username']).id
        return render_template('welcome.html', username=username, user_id=user_id)
    else:
        username = "Not logged in"
        return render_template('welcome.html', username=username)
    
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')


@app.route('/register', methods=['GET'])
def get_register():
    connection = get_flask_database_connection(app)
    return render_template('register_user.html')

@app.route('/register', methods=['POST'])
def send_new_registration():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    new_user = User(None, request.form['username'], request.form['password'])
    repository.create(new_user)
    return f'You have successfully registered'

# @app.route('/index', methods=['GET'])
# def get_all_spaces():
#     connection = get_flask_database_connection(app)


@app.route('/login', methods=['GET'])
def display_login_prompt():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    _connection = get_flask_database_connection(app)
    users_repository = UserRepository(_connection)
    attempted_user = request.form['username']
    password = request.form['password']
    if attempted_user in users_repository.all():
        if password == users_repository.find_by_username(attempted_user).password:
            session['username'] = attempted_user
            return redirect('/')
    else:
        return redirect('/login')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    session['username'] = None
    return redirect('/')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))


