import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mtgopen.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        
        return render_template("index.html")
    else:
       
        return redirect("/")
    
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation of passewordis correct

        elif password != confirmation:
            return apology("confirmation must match", 400)

        # Check password min 8 chars
        if len(password) < 8:
            return apology("password min 8 characters", 400)

        # Check password contains non alphanumberic numbers etc
        caps = False
        lower = False
        numeric = False
        nonalpha = False
        for char in password:
            if char.isupper():
                caps = True
            if char.islower():
                lower = True
            if char.isdigit():
                numeric = True
            if char.isalnum():
                nonalpha = True
        if not caps:
            return apology("at least 1 capital letter", 400)
        if not lower:
            return apology("at least 1 lower case letter", 400)
        if not numeric:
            return apology("at least 1 number", 400)
        if not nonalpha:
            return apology("at least 1 symbol", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) > 0:
            return apology("username already in use", 400)

        # Register new user
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?);",
            username,
            generate_password_hash(password),
        )
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    if request.method == "GET":
        return render_template("game.html")
    else:
        return render_template("index.html")
    
@app.route("/addfriend", methods=["GET", "POST"])
@login_required
def addfriend():
    if request.method == "GET":
        return render_template("addfriend.html", id=session["user_id"])
    else:
        friendid = request.form.get("id")
        # Ensure username was submitted
        if not friendid:
            return apology("must provide a friend id", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", friendid)

        # Ensure username exists
        if len(rows) == 0:
            return apology("could not find this user id", 400)
        elif int(friendid) == session["user_id"]:
            return apology("you can't be your own friend...", 400)
        # Check if they are already friends
        friendList = db.execute("SELECT friends FROM users WHERE id=?;", session["user_id"])
        alreadyfriends = False
        if any(friendList[0].values()) == True:
            friendListString = friendList[0]['friends']
            for friend in friendListString.split(","):
                if friend == friendid:
                    alreadyfriends = True
        if alreadyfriends:
            return apology("This person is already your friend", 400)
        
        friendReqString = ''
        # Check if a friend request has already been made
        friendReqList = db.execute("SELECT friendrequests FROM users WHERE id=?;", friendid)
        alreadyrequested = False
        if any(friendReqList[0].values()) == True:
            print("debug01")
            friendReqString = friendReqList[0]['friendrequests']
            print(friendReqString)
            if int(friendReqString) == session["user_id"]:
                alreadyrequested = True
            for req in friendReqString.split(","):
                if req == session["user_id"]:
                    alreadyrequested = True
        if alreadyrequested:
            return apology("This person has your friend request pending", 400)

        # Add friend request
        
        if any(friendReqList[0].values()) == False:
            friendReqString = friendid
            print(friendReqString)
        else:
            friendReqString = friendReqList[0]['friendrequests'] + ',' + friendid
        print(friendReqString)
        db.execute("UPDATE users SET friendrequests=? WHERE id=?;", session["user_id"], friendReqString)
        return render_template("index.html")
    
@app.route("/friends", methods=["GET", "POST"])
@login_required
def friends():
    friends = db.execute("SELECT * FROM users JOIN friends ON users.id= friends.user1 WHERE ;")
    requests = db.execute("SELECT friendrequests FROM users WHERE id=?;", session["user_id"])
    friendReqList = []
    if any(requests[0].values()) == True:
        friendReqList = requests[0]['friendrequests'].split(",")
    requestNames = []
    for reqID in friendReqList:
        requestDict = db.execute("SELECT username FROM users WHERE id=?;", reqID)
        requestNames.append(requestDict[0]['username'])

    friends = db.execute("SELECT friends FROM users WHERE id=?;", session["user_id"])
    friendList = []
    if any(friends[0].values()) == True:
        friendList = friends[0]['friends'].split(",")
    friendNames = []
    for friendID in friendList:
        friendDict = db.execute("SELECT username FROM users WHERE id=?;", friendID)
        friendNames.append(friendDict[0]['username'])

    if request.method == "GET":


        return render_template("friends.html", requests=requestNames, friends=friendNames)
    else:
        user = request.form.get("user")
        reply = request.form.get("reply")
        print(reply)
        # get userid from username
        userID = db.execute("SELECT id FROM users WHERE username=?", user)[0]['id']
        if reply == "accept":
            print("debug02")
            friends = db.execute("SELECT friends FROM users WHERE id=?;", session["user_id"])
            if (friends[0]['friends']):
                newFriendListString = friends[0]['friends'] + ',' + str(userID)
            else:
                newFriendListString = userID
            db.execute("UPDATE users SET friends=? WHERE id=?;", newFriendListString, session["user_id"])

            friends = db.execute("SELECT friends FROM users WHERE id=?;", str(userID))
            if (friends[0]['friends']):
                newFriendListString = (friends[0]['friends']) + ',' + str(session["user_id"])
            else:
                newFriendListString = session["user_id"]
            db.execute("UPDATE users SET friends=? WHERE id=?;", newFriendListString, userID)
        requests = db.execute("SELECT friendrequests FROM users WHERE id=?;", session["user_id"])
        friendReqList = []
        friendReqList = requests[0]['friendrequests'].split(",")
        friendReqList.remove(str(userID))
        if friendReqList:
            newReqListString = ','.join(friendReqList)
            db.execute("UPDATE users SET friendrequests=? WHERE id=?;", newReqListString, session["user_id"])
        else:
            db.execute("UPDATE users SET friendrequests='' WHERE id=?;", session["user_id"])

        return render_template("friends.html", requests=requestNames, friends=friendNames)