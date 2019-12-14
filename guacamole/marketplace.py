import firebase

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from guacamole.auth import login_required

bp = Blueprint("marketplace", __name__, url_prefix="/marketplace")


@bp.route("/", methods=("GET", "POST"))
def index():
    """Show all the posts, most recent first."""
    posts = firebase.db.child("marketplace").child("posts").get().each()
    if posts == None:
        posts = []
    print(posts[0].val()["deadline"])
    from datetime import datetime
    return render_template("marketplace/index.html", posts=posts, utcFromTimestamp=datetime.utcfromtimestamp)
        

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        budget = request.form["budget"]
        deadline = request.form["deadline"]
        payment = request.form["payment"]
        body = request.form["body"]

        error = None

        if not title:
            error = "Title is required."
        if error is not None:
            flash(error)
        else:
            from datetime import datetime
            import calendar

            d = datetime.utcnow()
            unixtime = calendar.timegm(d.utctimetuple())
            post = {
                "title":title,
                "deadline":deadline,
                "budget":budget,
                "payment":payment,
                "body": body,
                "author": g.user["localId"],
                "timestamp": unixtime
            }
            firebase.db.child("marketplace").child("posts").push(post)
            return redirect(url_for("marketplace.index"))

    return render_template("marketplace/create.html")


@bp.route("/<string:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = firebase.db.child("marketplace").child("posts").child(id).get()
    if request.method == "POST":
        title = request.form["title"]
        budget = request.form["budget"]
        deadline = request.form["deadline"]
        payment = request.form["payment"]
        body = request.form["body"]
        post = {
                "title":title,
                "deadline":deadline,
                "budget":budget,
                "payment":payment,
                "body": body,
            }
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            firebase.db.child("marketplace").child("posts").child(id).update(post)
            return redirect(url_for("marketplace.index"))

    return render_template("marketplace/update.html", post=post)


@bp.route("/<string:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = firebase.db.child("marketplace").child("posts").child(id).get()
    return redirect(url_for("marketplace.index"))


@bp.route("/<string:id>/bid", methods=("GET", "POST"))
@login_required
def bid(id):   
    """Bid on a post if the current user is not author."""
    post = firebase.db.child("marketplace").child("posts").child(id).get()
    if request.method == "POST":
        price = request.form["price"]
        delivery = request.form["delivery"]
        payment = request.form["payment"]
        body = request.form["body"]

        error = None

        from datetime import datetime
        import calendar

        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())
        bid = {
            "post":id,
            "price":price,
            "delivery":delivery,
            "payment":payment,
            "body": body,
            "author": g.user["localId"],
            "timestamp": unixtime
        }
        firebase.db.child("marketplace").child("bids").push(bid)
        return redirect(url_for("marketplace.index"))
    from datetime import datetime
    return render_template("marketplace/bid.html", post=post, utcFromTimestamp=datetime.utcfromtimestamp)


