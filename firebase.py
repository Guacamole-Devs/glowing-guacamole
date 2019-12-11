import pyrebase

config = {
    "apiKey": "AIzaSyCj4IEUIXULGHR-gXXMlTIZDPpi61vXQyI",
    "authDomain": "dollargig-firebase.firebaseapp.com",
    "databaseURL": "https://dollargig-firebase.firebaseio.com",
    "projectId": "dollargig-firebase",
    "storageBucket": "dollargig-firebase.appspot.com",
    "messagingSenderId": "2983760753",
    "appId": "1:2983760753:web:cb0297d846ec5213c59cd0"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()