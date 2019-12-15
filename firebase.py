import pyrebase

config = eval(open("cred.txt").read())
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

auth.sign_in_with_email_and_password("test1@login.noahkamara.com","123456")