import os
from lib.user_repository import *
from lib.space_repository import *
from flask import Flask, request, render_template, session, redirect
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.user import User

app = Flask(__name__)
app.secret_key = 'this_is_a_super_secret_key'

# WELCOME ROUTES
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
    
# WELCOME ROUTES
# REGISTER ROUTES
@app.route('/register', methods=['GET'])
def display_register_page():
    return render_template('register_user.html')

@app.route('/register', methods=['POST'])
def send_new_registration():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    valid_input = False
    username = request.form['username']
    password1 = request.form['password']
    password2 = request.form['confirm_password']
    password = password1 if password1 == password2 and (password1!= None) else None
    valid_input = username != '' and password != '' and password != None
    if valid_input == True:
        new_user = User(None, username, password)
        repository.create(new_user)
        login()
        return redirect('/')
    else:
        return redirect('/register') 

# REGISTER ROUTES
# LOGIN ROUTES
@app.route('/login', methods=['GET'])
def display_login_prompt():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    _connection = get_flask_database_connection(app)
    users_repository = UserRepository(_connection)
    attempted_user = request.form['username']
    password = request.form['password']
    if attempted_user in users_repository.list_all_usernames():
        if password == users_repository.find_by_username(attempted_user).password:
            session['username'] = attempted_user
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return redirect('/login')

# LOGIN ROUTES
# SPACES ROUTES
@app.route('/spaces', methods=['GET'])
def display_spaces_page():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.all()
    return render_template('spaces.html', spaces=spaces)
# SPACES ROUTES
# LOGOUT ROUTES
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    session['username'] = None
    return redirect('/')
# LOGOUT ROUTES

@app.route('/spaces/new', methods=['GET'])
def new_space_form():
    return render_template('create_new_space.html')

@app.route('/spaces/new', methods=['POST'])
def create_new_space():
    _connection = get_flask_database_connection(app)
    spaces_repository = SpaceRepository(_connection)
    valid_new_space = False
    name = request.form['name']
    location = request.form['location']
    description = request.form['description']
    price_per_night = request.form['price_per_night']
    availability = request.form['availability']
    if name != '' and location != '' and description != '' and price_per_night != None:
        valid_new_space = True
    if valid_new_space:
        new_space = Space(None, name, location, description, availability, price_per_night, 1)
        spaces_repository.create(new_space)
        return redirect('/spaces')
    else:
        return redirect('/spaces/new')
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))


