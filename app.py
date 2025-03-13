import functools
import os
from flask import Flask, request, render_template, session, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.user import User
from lib.space_repository import SpaceRepository
from lib.space import Space
import smtplib
from email.message import EmailMessage
from lib.booking_repository import BookingRepository
from lib.booking import Booking
from dotenv import load_dotenv

load_dotenv()
gmail_secret = os.getenv("GOOGLE_APP_SECRET")

app = Flask(__name__)
app.secret_key = "this_is_a_super_secret_key"


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session or session["username"] == None:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function


def update_dates_dictionary_from_requested_dates_list(
    available_dates_dict, requested_dates_list
):
    for date in requested_dates_list:
        available_dates_dict[date] = False
    return available_dates_dict


# WELCOME ROUTES
@app.route("/", methods=["GET"])
def welcome():
    if session.get("username") == False:
        session["username"] = None
    if session.get("username") and session["username"] != None:
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
    next_url = request.form.get("next")
    if users_repository.check_password(attempted_user, password):
        session["username"] = attempted_user
        if next_url:
            return redirect(next_url)
        return redirect("/")
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
    start_date = request.form["start_date"]  # for the available dates dict
    end_date = request.form["end_date"]  # for the available dates dict
    image_url = (
        request.form["image_url"]
        if request.form["image_url"] != ""
        else "https://upload.wikimedia.org/wikipedia/commons/3/3b/Picture_Not_Yet_Available.png"
    )
    user_id = users_repository.find_by_username(session["username"]).id
    if (
        name != "" and location != "" and description != "" and price_per_night != None
    ):  # and start_date != None and end_date != None:
        valid_new_space = True
    if valid_new_space:
        new_space = Space(
            None,
            name,
            location,
            description,
            price_per_night,
            start_date,
            end_date,
            image_url,
            user_id,
        )
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

    founders = [
        {
            "name": "Andrew Pang",
            "image": "https://ca.slack-edge.com/T03ALA7H4-U089649MMQC-c22713126f2f-512",
            "ghprofile": "https://github.com/pangacm",
        },
        {
            "name": "Will Egerton",
            "image": "https://ca.slack-edge.com/T03ALA7H4-U089SD1E83A-9fef626c96b4-512",
            "ghprofile": "https://github.com/WEgerton",
        },
        {
            "name": "Jack Misner",
            "image": "https://ca.slack-edge.com/T03ALA7H4-U089CLJQMKK-9b3e6a0e85de-512",
            "ghprofile": "https://github.com/jackmisner",
        },
        {
            "name": "Joseph Ducrocq",
            "image": "https://ca.slack-edge.com/T03ALA7H4-U088KDUVD0F-c40d5d623bb1-512",
            "ghprofile": "https://github.com/JosephDucrocq",
        },
        {
            "name": "John Rothera",
            "image": "https://ca.slack-edge.com/T03ALA7H4-U0893FT4Q7M-cd53f939148c-512",
            "ghprofile": "https://github.com/JohnRothera",
        },
        {
            "name": "Luis Moseley-Robinson",
            "image": "https://ca.slack-edge.com/T03ALA7H4-U089649HLAG-f31e2ebbfeab-512",
            "ghprofile": "https://github.com/fastongithub",
        },
    ]

    username = _get_logged_in_user()
    return render_template("about.html", spaces=spaces, username=username, founders=founders)

@app.route("/user/<username>", methods=["GET"])
@login_required
def get_individual_user(username):
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    space_repository = SpaceRepository(connection)

    user = user_repository.find_by_username(username)
    spaces = space_repository.find_by_user_id(user.id)
    logged_in_username = f"{session['username']}"
    if logged_in_username != username:
        return redirect('/')
    return render_template(
        "single_user.html",
        user=user,
        spaces=spaces,
        username=username,
        logged_in_username=logged_in_username,
    )


@app.route("/book/<space_id>", methods=["GET"])
@login_required
def book_space(space_id):
    """Display booking page for a space with an interactive calendar"""
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(space_id)
    username = f"{session['username']}"

    return render_template("booking.html", username=username, space=space)


@app.route("/book/<space_id>/confirm", methods=["POST"])
@login_required
def confirm_booking(space_id):
    """Create a new booking and show confirmation page"""
    # Get form data
    check_in_date = request.form.get("check_in_date")
    check_out_date = request.form.get("check_out_date")
    nights = int(request.form.get("nights", 0))
    total_price = float(request.form.get("total_price", 0))

    # Calculate subtotal and service fee (assuming 12% service fee)
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    user_repository = UserRepository(connection)
    booking_repository = BookingRepository(connection)

    space = space_repository.find(space_id)
    user = user_repository.find_by_username(session["username"])

    subtotal = float(space.price_per_night) * nights
    service_fee = round(subtotal * 0.12, 2)  # 12% service fee

    # Create new booking
    from lib.booking import Booking

    booking = Booking(
        id=None,
        start_date=check_in_date,
        end_date=check_out_date,
        user_id=user.id,
        space_id=space_id,
        subtotal=subtotal,
        service_fee=service_fee,
        total=total_price or (subtotal + service_fee),
        approved=False,
    )

    # Save booking to database
    booking = booking_repository.create(booking)

    updated_dates_dict = update_dates_dictionary_from_requested_dates_list(
        space.dates_available_dict, booking.requested_dates_list
    )
    space_repository.update_available_dates(updated_dates_dict, booking.space_id)
    # Redirect to confirmation page
    return redirect(f"/bookings/{booking.id}/confirmation")


@app.route("/bookings/<booking_id>/confirmation", methods=["GET"])
@login_required
def booking_confirmation(booking_id):
    """Show booking confirmation details"""
    # Get booking details
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    space_repository = SpaceRepository(connection)

    booking = booking_repository.find(booking_id)

    # Ensure the booking exists
    if booking is None:
        return redirect("/spaces")

    # Get space details
    space = space_repository.find(booking.space_id)

    username = session["username"]
    return render_template(
        "booking_confirmation.html", username=username, booking=booking, space=space
    )


@app.route("/user/<username>/bookings", methods=["GET"])
@login_required
def user_bookings(username):
    """Show a user's bookings"""


    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    booking_repository = BookingRepository(connection)
    space_repository = SpaceRepository(connection)

    user = user_repository.find_by_username(username)
    bookings = booking_repository.find_by_user(user.id)

    # Get space details for each booking
    booking_details = []
    for booking in bookings:
        space = space_repository.find(booking.space_id)
        booking_details.append({"booking": booking, "space": space})

    return render_template(
        "user_bookings.html", username=username, booking_details=booking_details
    )


# ABOUT ROUTE

# CONTACT ROUTE

@app.route("/contact", methods=["GET"])
def contact():
    username = _get_logged_in_user()
    return render_template("contact.html", username=username)

@app.route("/form", methods=["POST"])
def form():
    name = request.form.get("name")
    email = request.form.get("email")
    comment = f"SENT FROM:\n {email}\n\nMESSAGE:\n"
    comment += request.form.get("comment") 

    work_email = "makersbnb2025@gmail.com"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("makersbnb2025@gmail.com", gmail_secret)

    email_list = [
        {
            "email": email,
            "content": f"Thank you {name}!\n\nYour comment has been received and we will respond within 2 working days.",
            "subject": 'Makersbnb: We\'re Here to Help with Your Issue',
        },
        {
            "email": work_email,
            "content": comment,
            "subject": f"DO NOT REPLY - Query ticket raised from: {name}"}
            ]
    
    for mail in email_list:
        msg = EmailMessage()
        msg.set_content(mail['content'], subtype="plain", charset='us-ascii')
        msg['Subject'] = mail['subject']
        msg['From'] = work_email
        msg['To'] = mail['email']
        server.send_message(msg)
    
    server.quit()

    # Check if user is logged in
    username = _get_logged_in_user()
    return render_template("form.html", username=username, name=name)


# CONTACT ROUTE

@app.errorhandler(404)
@app.errorhandler(405)
def handle_http_error(e):
    username = _get_logged_in_user()
    error_code = e.code
    return render_template(f'{error_code}.html', username=username), error_code

def _get_logged_in_user():
    if "username" in session and session["username"] is not None:
        return session["username"]
    return "Not logged in"

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
