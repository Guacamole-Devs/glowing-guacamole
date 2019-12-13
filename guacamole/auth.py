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
        if g.user == None:
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
        g.user = firebase.auth.current_user


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]
        error = None
        try:
            user = firebase.auth.create_user_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']["message"]
        if error is None:
            # store the user id in a new session and return to the index
            firebase.auth.send_email_verification(user["idToken"])
            user = firebase.auth.current_user
            profile = { "username": username }
            firebase.db.child("users").child(user["localId"]).set(profile)
            session.clear()
            session["user_id"] = user["localId"]
            session["user_token"] = user["idToken"]
            flash("Please verify")
            return redirect(url_for("marketplace.index"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login(error = None):
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        email = request.form["email#+"]
        password = request.form["password"]
        error = None
        try:
            user = firebase.auth.sign_in_with_email_and_password(email, password)
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']["message"]

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["localId"]
            session["user_token"] = user["idToken"]
            return redirect(url_for("marketplace.index"))
        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("marketplace.index"))

