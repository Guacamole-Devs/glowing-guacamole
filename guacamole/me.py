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

@bp.route("", methods=("GET", "POST"))
@login_required
def profile():
    return render_template("profile/profile.html")

@bp.route("/posts", methods=("GET", "POST"))
@login_required
def posts():
    """Show users posts, most recent first."""
    myPosts = firebase.db.child("marketplace").child("posts").order_by_child("author").get()
    from datetime import datetime
    return render_template("profile/posts.html", posts=myPosts, utcFromTimestamp=datetime.utcfromtimestamp)

@bp.route("/post/<string:id>", methods=("GET", "POST"))
@login_required
def post(id):
    """Show post overview"""
    post = firebase.db.child("marketplace").child("posts").child(id).get()
    bids = firebase.db.child("marketplace").child("bids").order_by_child("post").equal_to(id).get()
    print(post)
    from datetime import datetime
    return render_template("profile/post_detail.html", post=post, bids=bids, utcFromTimestamp=datetime.utcfromtimestamp)

@bp.route("/bids", methods=("GET", "POST"))
@login_required
def bids():
    """Show users posts, most recent first."""
    myBids = firebase.db.child("marketplace").child("bids").order_by_child("author").equal_to(g.user["localId"]).get()
    from datetime import datetime
    return render_template("profile/bids.html", bids=myBids, utcFromTimestamp=datetime.utcfromtimestamp)