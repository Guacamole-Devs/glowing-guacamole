import pyrebase

config = eval(open("cred.txt").read())
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

import requests
import json

class Profile:
    def __init__(self, uid):
        self.uid = uid
        profile_dict = db.child('users').child(self.uid).get()
        self.username = profile_dict.val()['username']
        self.created_at = profile_dict.val()['created_at']
        self.photo_url = profile_dict.val()['photo_url']

def getUserProfile(id):
    profile = db.child("users").child(id).get()
    return profile
    


class User:
    profile = None
    user = None
    def __init__(self, user):
        self.user = user
        self.idToken = user['idToken']
        self.localId = user['localId']
        self.email = user['email']
        self.isEmailVerified = None
        self.username = None
        self.photoUrl = None
        self.isDisabled = None
        self.createdAt = None

        self.getAccountInfo()

    def getAccountInfo(self):
        if not User is None:
            url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={}".format(auth.api_key)
            headers = {'content-type': 'application/json'}
            data = {'idToken': self.idToken}

            json_data = json.dumps(data)
            response = requests.post(url, data=json_data, headers=headers)
            response_json = json.loads(response.text)
            
            userInfo = response_json.get("users")[0]
            self.isEmailVerified = userInfo.get("emailVerified")
            self.createdAt = userInfo.get("createdAt")
            self.photoUrl = userInfo.get("photoUrl")
            self.isDisabled = (userInfo.get("disabled") == True)
            self.username = userInfo.get("providerUserInfo")[0].get("displayName")
                
    def changeAccountInfo(self, username = None, photoUrl = None):

        url ="https://identitytoolkit.googleapis.com/v1/accounts:update?key={}".format(auth.api_key)
        headers = {'content-type': 'application/json'}
        data = {
            'idToken': self.idToken,
            'returnSecureToken': True
            }
        if username is not None:
            data['displayName'] = username
            db.child("users").child(self.localId).child("profile").set({'username': username})

        if photoUrl is not None:
            data['photoUrl'] = photoUrl
            db.child("users").child(self.localId).child("profile").set({'photoUrl': photoUrl})

        json_data = json.dumps(data)
        response = requests.post(url, data=json_data, headers=headers)
        response_json = json.loads(response.text)

    def printUser(self):
        print("""
        ID LOCAL: {}
           EMAIL: {}
        VERIFIED: {}
        USERNAME: {}
           PHOTO: {}
        DISABLED: {}
         CREATED: {}
        """.format(self.localId, self.email, self.isEmailVerified, self.username, self.photoUrl, self.isDisabled, self.createdAt))