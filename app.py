import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
        """Show portfolio of stocks"""
        holdings = db.execute(
            "SELECT * FROM holdings WHERE userid = ?;", session["user_id"]
        )
        total = 0
        availablecash = db.execute(
            "SELECT cash FROM users WHERE id = ?;", session["user_id"]
        )
        for holding in holdings:
            # loop the list of stock dicts
            holding.update({"current_price": lookup(holding["stock"])["price"]})
            holding["current_value"] = holding["current_price"] * holding["shares"]
            total += holding["current_value"]

            holding["current_value"] = usd(holding["current_value"])
            holding["current_price"] = usd(holding["current_price"])

        totalassets = usd(total + availablecash[0]["cash"])
        totalcash = usd(availablecash[0]["cash"])
        total = usd(total)
        return render_template(
            "index.html",
            holdings=holdings,
            total=total,
            totalcash=totalcash,
            totalassets=totalassets,
        )
    else:
        # if arrived by post process adding cash
        addcash = request.form.get("addcash")
        if not addcash.isnumeric():
            return apology("please enter a number", 400)
        addcash = int(addcash)
        availablecash = db.execute(
            "SELECT cash FROM users WHERE id = ?;", session["user_id"]
        )
        cash = availablecash[0]["cash"] + addcash
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash, session["user_id"])
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
        print(username)
        print(password)
        print(confirmation)
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
