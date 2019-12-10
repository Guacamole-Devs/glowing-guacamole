import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from random import randint
from guacamole.db import get_db,close_db
from guacamole.sendemail import sendmail
bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view




@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = "User {0} is already registered.".format(username)
        elif (
            db.execute("SELECT id FROM user WHERE email = ?", (email,)).fetchone()
            is not None
        ):
            error = "email {0} is already registered.".format(email)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            code = randint(1000,10000)
            db.execute(
                "INSERT INTO user (username, email, password, verify_key) VALUES (?, ?, ?, ?)",
                (username, email, generate_password_hash(password), code)
            )
            db.commit()
            sendmail(email,code,username)
            flash("Check your Inbox: Please validate your Account.")
                        
            return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
        elif user["email_verified"] == 0:
            error = "Email not verified."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))

@bp.route("/validate/")
def validate():
    username = request.args.get("username")
    code = request.args.get("code")
    if username is None or code is None:
        return render_template("auth/validate.html")
    else:
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        if user["email_verified"] == 1:
            return redirect(url_for("auth.login"))
        else:
            if int(code) == int(user["verify_key"]):
                db.execute(
                    "UPDATE user SET email_verified=1 WHERE username=(?)", (username,))
                db.commit()
                flash("You can log in now! You are verified!")
                return redirect(url_for("auth.login"))
            else:
                error = "wrong code/link"
                flash(error)
                return render_template("auth/validate.html")






