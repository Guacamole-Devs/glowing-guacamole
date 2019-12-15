import firebase
from flask import Blueprint, request, g, session,render_template
from flask import jsonify
from guacamole.auth import login_required
bp = Blueprint("messaging_system", __name__, url_prefix="/messaging_system")



def send_message_as_bidder_by_post(message, post_id):
    """pushes message to firebase as someone who bid"""
    receiver = firebase.db.child("marketplace").child("posts").child(post_id).child("author").get().val()    
    from datetime import datetime
    import calendar
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    firebase.db.child("messaging_system").push({"message": message, "post_id": post_id, "receiver": receiver, "sender": session["user_id"],"timestamp":unixtime})

def send_message_as_poster(message, post_id, receiver):
    """pushes message to firebase as someone that made a post"""
    from datetime import datetime
    import calendar
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    firebase.db.child("messaging_system").messaging_system.push({"message": message, "post_id": post_id, "receiver": receiver, "sender": session["user_id"],"timestamp":unixtime})

def get_every_chat_from_post(post_id):
    messagesofpost = firebase.db.child("messaging_system").child(post_id).get().val()
    return messagesofpost

def get_chat_between_poster_and_user(post_id, user_id):
    yourmessages = firebase.db.child("messaging_system").child(post_id).order_by_child("sender").equal_to(session["user_id"]).get().val()
    biddermessages = firebase.db.child("messaging_system").child(post_id).order_by_child("sender").equal_to(user_id).get().val()
    return yourmessages, biddermessages

@bp.route("/send",methods=["GET","POST"])
@login_required
def send_message():
    if request.method == "POST":
        send_message_as_bidder_by_post(request.form.get("message"), request.form.get("post_id"))
        return render_template("messaging_system/chat.html")
    return render_template("messaging_system/chat.html")
    

