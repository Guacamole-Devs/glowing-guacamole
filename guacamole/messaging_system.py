import firebase
from flask import Blueprint, request, g, session, render_template
from flask import jsonify
from guacamole import socketio
from guacamole.auth import login_required
from flask import jsonify
from flask_socketio import join_room

bp = Blueprint("messaging_system", __name__, url_prefix="/messaging_system")


def send_message(message, room):
    """pushes message to firebase as someone who bid"""
    from datetime import datetime
    import calendar

    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    firebase.db.child("messaging_system").child(room).push(
        {"message": message, "sender": session["user_id"], "timestamp": unixtime,}
    )


@bp.route("/chat/<room>")
def sendroom(room):
    from datetime import datetime

    messages = firebase.db.child("messaging_system").child(room).get()
    listofmessagesasstring = []
    try:
        for message in messages.each():
            listofmessagesasstring.append(message.val())
    except:
        pass
    print(listofmessagesasstring)
    return render_template(
        "messaging_system/chat.html",
        utcFromTimestamp=datetime.utcfromtimestamp,
        listofmessagesasstring=listofmessagesasstring,
        room=room,
    )


@socketio.on("join")
def join(room):
    join_room(room)


@socketio.on("message")
def handle_message(message):
    print("received message: " + message.get("message"))
    try:
        send_message(message.get("message"), message.get("room"))
        socketio.send(message.get("message"))
    except:
        print("DU BIST NICHT EINGELOGGT")

