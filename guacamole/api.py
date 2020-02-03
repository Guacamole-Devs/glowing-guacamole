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
from flask import jsonify
from enum import Enum
from datetime import datetime

class QueryParameter(Enum):
    deadline = "deadline"
    published = "timestamp"
    budget = "budget"

def post_query_response(posts):
    response = {
        'timestamp': datetime.utcnow().timestamp(),
        'posts': []
    }
    for post in posts:
        post_json = {
            'key': post.key(),
            'timestamp': post.val()['timestamp'],
            'author': post.val()['author'],
            'author_user': post.val().get('author_user'),
            'title': post.val()['title'],
            'body': post.val()['body'],
            'budget': post.val()['budget'],
            'deadline': post.val()['deadline'],
            'payment': post.val()['payment'],
            'faq': []
        }
        if post.val().get('faq') != None:
            for faq in post.val()['faq']:
                faq_json = {

                }
                post_json['faq'].append(faq_json)
        response['posts'].append(post_json)
    return jsonify(response)

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/", methods=("GET", "POST"))
def apiHelp():
    data = {
        "onlyActive": True,
        "sortedBy": QueryParameter.deadline.value,
        "query": None
    }
    import requests
    response = requests.post("http://127.0.0.1:5000/api/posts", json=data)
    print(response.url)
    print(response)
    return response.content


@bp.route("/posts", methods=("GET", "POST"))
def queryPosts():
    if request.method == "POST":
        json_data = request.json
        only_active = json_data.get('onlyActive')
        sorted_by = QueryParameter(json_data.get('sortedBy'))
        all_posts = firebase.db.child("marketplace").child("posts").order_by_child(sorted_by.value).get().each()
        filteredPosts = []
        if all_posts == None:
            all_posts = []
        if only_active:
            for post in all_posts:
                deadline = post.val()['deadline']
                deadlineDate = datetime.strptime(deadline, "%Y-%m-%d")
                if datetime.utcnow() < deadlineDate:
                    filteredPosts.append(post)
        else:
            filteredPosts = all_posts
        if sorted_by in [QueryParameter.budget, QueryParameter.published]:
            print("REVERSED")
            filteredPosts.reverse()
        response = post_query_response(filteredPosts)
        return response
    return "API HELP",200
    

@bp.route("/test")
def testPage():
    return render_template("test.html")

@bp.route("/apitest")
def testJson():
    response = {
        'timestamp': 0,
        'posts': []
    }
    for i in range(1,5):
        post_json = {
            'key': "ABCTESTKEY_0{}".format(i),
            'timestamp': 0,
            'author': "ABCTESTAUTHOR",
            'author_user': "noahkamara01",
            'title': "#{} Hey guys help me please".format(i),
            'body': "LOorem Ipsum Dolorem sit",
            'budget': "123141",
            'deadline': "2019-12-31",
            'payment': "nudes"
        }
        response['posts'].append(post_json)
    return jsonify(response)


# <div class="shadow-sm card" style="width: 100%; margin-bottom: 10px" id="card">
#     <div class="card-body">
#         <div class="row card-title" style="width: 100%">
#             <div class="col-sm-9"><h5 id="post_title">## TITLE GOES HERE ##</h5></div>
#             <div class="col-sm-3">
#                 <h5>
#                     <span class="pull-right">
#                         <i class="fas fa-dollar-sign"></i> 
                        
#                     </span>
#                 </h5>
#             </div>
#         </div>
#     </div>
# </div>