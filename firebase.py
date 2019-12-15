import pyrebase

config = eval(open("cred.txt").read())
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

