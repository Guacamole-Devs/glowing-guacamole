import firebase
from flask import Blueprint, request, g, session, render_template
from flask import jsonify
from guacamole import socketio
from guacamole.auth import login_required
from flask import jsonify

bp = Blueprint("messaging_system", __name__, url_prefix="/messaging_system")


def send_message(message, post_id, receiver):
    """pushes message to firebase as someone who bid"""
    from datetime import datetime
    import calendar

    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    firebase.db.child("messaging_system").push(
        {
            "message": message,
            "post_id": post_id,
            "receiver": receiver,
            "sender": session["user_id"],
            "timestamp": unixtime,
        }
    )


def get_chat_between_poster_and_user(post_id, user_id):
    messages = [
        x.val()
        for x in firebase.db.child("messaging_system")
        .order_by_child("post_id")
        .equal_to(post_id)
        .order_by_child("sender")
        .equal_to(user_id)
        .get()
    ]
    biddermessages = [
        x.val()
        for x in firebase.db.child("messaging_system")
        .order_by_child("post_id")
        .equal_to(post_id)
        .order_by_child("receiver")
        .equal_to(user_id)
        .get()
    ]
    messages.extend(biddermessages)
    messages.sort(key=lambda k: k["timestamp"])
    return messages


@bp.route("/send2")
def send2():
    return render_template("messaging_system/chat.html")


@bp.route("/send/<post_id>/<receiver>", methods=["GET", "POST"])
def send(post_id, receiver):
    from datetime import datetime

    if request.method == "POST":
        send_message(request.form.get("message"), post_id, receiver)
    return jsonify(get_chat_between_poster_and_user(post_id, session.get("user_id")))


@login_required
@bp.route("/mychats")  # chatid fehlt
def mychats():
    print(session.get("user_id"))
    chats = [
        x.val()
        for x in (
            firebase.db.child("marketplace")
            .child("bids")
            .order_by_child("author")
            .equal_to(session.get("user_id"))
            .get()
            .each()
        )
    ]
    posts = [
        x.key()
        for x in (
            (
                firebase.db.child("marketplace")
                .child("posts")
                .order_by_child("author")
                .equal_to(session.get("user_id"))
                .get()
                .each()
            )
        )
    ]
    # print(posts)
    postchat = []
    for key in posts:
        try:
            postchat.append(
                firebase.db.child("marketplace")
                .child("bids")
                .order_by_child("post")
                .equal_to(key)
                .get()
                .val()
            )
        except:
            pass

    chats.extend(postchat)
    return jsonify(chats.sort(key=lambda k: k["timestamp"]))


def listchats():
    print(session.get("user_id"))
    chats = [
        x.val()
        for x in (
            firebase.db.child("marketplace")
            .child("bids")
            .order_by_child("author")
            .equal_to(session.get("user_id"))
            .get()
            .each()
        )
    ]
    posts = [
        x.key()
        for x in (
            (
                firebase.db.child("marketplace")
                .child("posts")
                .order_by_child("author")
                .equal_to(session.get("user_id"))
                .get()
                .each()
            )
        )
    ]
    # print(posts)
    postchat = []
    for key in posts:
        try:
            postchat.append(
                firebase.db.child("marketplace")
                .child("bids")
                .order_by_child("post")
                .equal_to(key)
                .get()
                .val()
            )
        except:
            pass

    chats.extend(postchat)
    return chats.sort(key=lambda k: k["timestamp"])


@login_required
@bp.route("/chat/<chat_id>")
def chat(chat_id):
    if chat_id not in [item.get("author") for item in listchats()]:
        return render_template("errorpages/404.html"), 404


@socketio.on("message")
def handle_message(message):
    print("received message: " + message)

