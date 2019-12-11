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

from guacamole.auth import login_required
bp = Blueprint("me", __name__, url_prefix="/me")

@bp.route("/posts", methods=("GET", "POST"))
@login_required
def posts():
    """Show users posts, most recent first."""
    #firebase.db.child("marketplace").child("bids").child(id).child("bids").push(post)
    myPosts = firebase.db.child("marketplace").child("posts").order_by_child("author").get()
    from datetime import datetime
    return render_template("profile/posts.html", posts=myPosts, utcFromTimestamp=datetime.utcfromtimestamp)