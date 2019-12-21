import functools

import firebase
import requests
import json
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

bp = Blueprint("auth", __name__, url_prefix="/auth")
def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            if g.user is None:
                return redirect(url_for("auth.login"))
        except AttributeError:
            flash("You have been logged out")
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
        if firebase.auth.current_user is not None:
            g.user = firebase.User(firebase.auth.current_user)
        else:
            session.clear()


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]
        username = request.form["username"]
        error = None
        try:
            response = firebase.auth.create_user_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']["message"]
        if error is None:
            # store the user id in a new session and return to the index
            user = firebase.User(response)
            firebase.auth.send_email_verification(user.idToken)
            firebase.auth.sign_in_with_email_and_password(email, password)
            user.changeAccountInfo(username)
            
            user = None
            flash("Check your Email")
            return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login(error = None):
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        session.clear()
        email = request.form["email"]
        password = request.form["password"]
        error = None
        try:
            response = firebase.auth.sign_in_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']["message"]

        if error is None:
            # store the user id in a new session and return to the index
            user = firebase.User(response)
            user.printUser()
            if user.isEmailVerified == False:
                flash("Verify your Email adress")
                session["user_token"] = user.idToken
                return redirect(url_for("auth.verify", email=email, password=password))
            session.clear()
            session["user_id"] = user.localId
            session["user_token"] = user.idToken
            return redirect(url_for("marketplace.index"))
        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    g.user = None
    return redirect(url_for("marketplace.index"))

@bp.route("/forgot", methods=("GET", "POST"))
def forgot():
    if request.method == "POST":
        email = request.form.get("email")
        
        error = None
        try:
            firebase.auth.send_password_reset_email(email)
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']["message"]

        if error is None:
            # store the user id in a new session and return to the index
            flash("Check your Email for Instruction on how to reset your password.")
            return redirect(url_for("auth.login"))    
        else:
            flash(error)
    return render_template("auth/forgot.html")

@bp.route("/verifyEmail", methods=("GET", "POST"))
def verify(email=None, password=None):
    if request.method == "POST":
        email = request.form.get("email")
        firebase.auth.send_email_verification(session["user_token"])
        session.clear()
        return render_template("auth/login.html")
    return render_template("auth/verify.html")