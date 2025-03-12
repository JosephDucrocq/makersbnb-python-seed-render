import os
from flask import Flask, request, render_template, session, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.user import User
from lib.space_repository import SpaceRepository
from lib.space import Space

app = Flask(__name__)
app.secret_key = "this_is_a_super_secret_key"


def login_required(func):
    def secure_function():
        if "username" not in session or session["username"] == None:
            session['url'] = url_for('create_new_space')
            return redirect(("/login"))
        return func()

    return secure_function


# WELCOME ROUTES
@app.route("/", methods=["GET"])
def welcome():
    if "username" in session and session["username"] != None:
        username = f"{session['username']}"
        _connection = get_flask_database_connection(app)
        users_repository = UserRepository(_connection)
        user_id = users_repository.find_by_username(session["username"]).id
        return render_template("welcome.html", username=username, user_id=user_id)
    else:
        username = "Not logged in"
        return render_template("welcome.html", username=username)


# WELCOME ROUTES


# REGISTER ROUTES
@app.route("/register", methods=["GET"])
def display_register_page():
    return render_template("register_user.html")


@app.route("/register", methods=["POST"])
def send_new_registration():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    valid_input = False
    username = request.form["username"]
    password1 = request.form["password"]
    password2 = request.form["confirm_password"]
    password = password1 if password1 == password2 and (password1 != None) else None
    valid_input = username != "" and password != "" and password != None
    if valid_input == True:
        new_user = User(None, username, password)
        repository.create(new_user)
        login()
        return redirect("/")
    else:
        return redirect("/register")


# REGISTER ROUTES


# LOGIN ROUTES
@app.route("/login", methods=["GET"])
def display_login_prompt():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    _connection = get_flask_database_connection(app)
    users_repository = UserRepository(_connection)
    attempted_user = request.form["username"]
    password = request.form["password"]
    if users_repository.check_password(attempted_user, password):
        session["username"] = attempted_user
        if 'url' in session:
            return redirect(session['url'])
        return redirect('/')
    else:
        return redirect("/login")


# LOGIN ROUTES


# LOGOUT ROUTES
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    session["username"] = None
    return redirect("/")


# LOGOUT ROUTES


# SPACES ROUTES
@app.route("/spaces", methods=["GET"])
def display_spaces_page():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.all()
    if "username" in session and session["username"] != None:
        username = f"{session['username']}"
        return render_template("spaces.html", spaces=spaces, username=username)
    else:
        username = "Not logged in"
        return render_template("spaces.html", spaces=spaces, username=username)


@app.route("/spaces/new", methods=["GET"])
@login_required
def new_space_form():
    username = f"{session['username']}"
    return render_template("create_new_space.html", username=username)
    # else:
    #     username = "Not logged in"
    #     return render_template("create_new_space.html", username=username)


@app.route("/spaces/new", methods=["POST"])
def create_new_space():
    _connection = get_flask_database_connection(app)
    users_repository = UserRepository(_connection)
    spaces_repository = SpaceRepository(_connection)
    valid_new_space = False
    name = request.form["name"]
    location = request.form["location"]
    description = request.form["description"]
    price_per_night = request.form["price_per_night"]
    start_date = request.form["start_date"] # for the available dates dict
    end_date = request.form["end_date"] # for the available dates dict
    image_url = request.form['image_url'] if request.form['image_url'] != '' else "https://upload.wikimedia.org/wikipedia/commons/3/3b/Picture_Not_Yet_Available.png"
    user_id = users_repository.find_by_username(session['username']).id
    if name != "" and location != "" and description != "" and price_per_night != None: #and start_date != None and end_date != None:
        valid_new_space = True
    if valid_new_space:
        new_space = Space(
            None, name, location, description, price_per_night, start_date, end_date, image_url, user_id)
        spaces_repository.create(new_space)
        return redirect("/spaces")
    else:
        return redirect("/spaces/new")


@app.route("/spaces/<space_id>", methods=["GET"])
def get_individual_space(space_id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(space_id)
    if "username" in session and session["username"] != None:
        username = f"{session['username']}"
        return render_template("single_space.html", username=username, space=space)
    else:
        username = "Not logged in"
        return render_template("single_space.html", username=username, space=space)


# SPACES ROUTES


# ABOUT ROUTE
@app.route("/about", methods=["GET"])
def display_about_page():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.all()
    founders = {
        "Andrew": "https://ca.slack-edge.com/T03ALA7H4-U089649MMQC-c22713126f2f-512",
        "Will": "https://ca.slack-edge.com/T03ALA7H4-U089SD1E83A-9fef626c96b4-72",
        "Jack": "https://ca.slack-edge.com/T03ALA7H4-U089CLJQMKK-9b3e6a0e85de-512",
        "Joseph": "https://ca.slack-edge.com/T03ALA7H4-U088KDUVD0F-c40d5d623bb1-512",
        "John": "https://ca.slack-edge.com/T03ALA7H4-U0893FT4Q7M-cd53f939148c-512",
        "Luis": "https://ca.slack-edge.com/T03ALA7H4-U089649HLAG-f31e2ebbfeab-512",
    }

    if "username" in session and session["username"] != None:
        username = f"{session['username']}"
        return render_template(
            "about.html", spaces=spaces, username=username, founders=founders
        )
    else:
        username = "Not logged in"
        return render_template(
            "about.html", founders=founders, spaces=spaces, username=username
        )


@app.route("/user/<username>", methods=["GET"])
def get_individual_user(username):
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    user = repository.find_by_username(username)
    if "username" in session and session["username"] != None:
        logged_in_username = f"{session['username']}"
        return render_template(
            "single_user.html", user=user, logged_in_username=logged_in_username
        )
    else:
        logged_in_username = "Not logged in"
        return render_template(
            "single_user.html", user=user, logged_in_username=logged_in_username
        )


# ABOUT ROUTE

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
