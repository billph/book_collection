from flask import render_template, url_for, redirect, request, flash, jsonify, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.controllers.social import bp
from app.models import User

# go to a specific profile
@bp.route("/user/<username>", methods=["GET"])
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()
    
    avail_activities = u.get_activities()
    activities = []
    for i in range(3):
        try:
            activities.append(avail_activities[i])
        except IndexError:
            activities.append(None)

    book_count = len(u.get_books())
    activities_count = (3 if len(avail_activities) >= 3 else len(avail_activities))
    return render_template("social/user_page.html", user=u, activities=activities, following_count=len(u.following),
                followers_count=len(u.followers), book_count=book_count, activities_count=activities_count, title=username)

# get bio from a post request and update it
@bp.route("/addbio", methods=["POST"])
@login_required
def add_bio():
    data = request.get_json()
    if data["username"] != current_user.username:
        return redirect(url_for("errors.bad_request"))
    u = User.query.filter_by(username=data["username"]).first()
    u.add_bio(data["bio"])
    return jsonify({"success": True})

# return a page that includes all profiles
@bp.route("/explore", methods=["GET"])
@login_required
def explore():
    users = User.query.all()
    return render_template("social/explore.html", users=users, title="Expore")

# follow a person. Takes in user id of that person
@bp.route("/social/follow", methods=["POST"])
@login_required
def follow():
    try: 
        data = request.get_json()
        username = data["username"]
        other_user = User.query.filter_by(username=username).first()
        if not other_user:
            return redirect(url_for("errors.bad_request"))
        if current_user.is_following(other_user):
            current_user.unfollow(other_user)
        else:
            current_user.follow(other_user)
    except:
        return redirect(url_for("errors.bad_request"))

    return jsonify({"success": True}), 200

# search user. takes in the username of that user
@bp.route("/search/user", methods=["GET"])
@login_required
def search_user():
    username = request.args.get('username')
    list_of_names = User.query.filter(User.username.like("%{}%".format(username)) | User.email.like("%{}%".format(username))).all()
    dic = {}
    item = []
    for i in list_of_names:
        try:
            dic[i.username] = dic[i.first_name] + dic[i.last_name]
            item.append({"fullname": i.firstname + i.lastname, "username": i.username})
        except KeyError:
            item.append({
                "fullname": "Foo Bar", 
                "username": i.username,
                "imageLink": i.add_avatar(1024),
                "profileLink": url_for('social.user', username=i.username)
            })
    dic["value"] = item
    return jsonify(dic)
