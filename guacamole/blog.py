from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from guacamole.auth import login_required
from guacamole.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username, deadline, budget, payment"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username, deadline, budget, payment"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


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
            db = get_db()
            db.execute(
                "INSERT INTO post (title, deadline, budget, payment, body, author_id) VALUES (?, ?, ?, ?, ?, ?)",
                (title, deadline, budget, payment, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

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
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, deadline = ?, budget = ?, payment = ?, body = ?WHERE id = ?", (title, deadline, budget, payment, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))


@bp.route("/<int:id>/bid", methods=("GET", "POST"))
@login_required
def bid(id):
    """Bid on a post if the current user is not author."""
    post = get_post(id, False)
    if request.method == "POST":
        price = request.form["price"]
        delivery = request.form["delivery"]
        payment = request.form["payment"]
        body = request.form["body"]

        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO bid (post_id, price, delivery, payment, body, author_id) VALUES (?, ?, ?, ?, ?, ?)",
                (id, price, delivery, payment, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/bid.html", post=post)


@bp.route("/me/posts", methods=("GET", "POST"))
@login_required
def posts():
    """Show users posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username, deadline, budget, payment"
        " FROM post p JOIN user u ON p.author_id = u.id WHERE author_id=?"
        " ORDER BY created DESC",(1,)
    ).fetchall()
    return render_template("profile/posts.html", posts=posts)