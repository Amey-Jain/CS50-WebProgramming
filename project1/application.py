import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = "3bslkj3s"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["POST","GET"])
def index():
    if bool(session) == False:
        #no users logged in
        return render_template("login.html")
    else :
        #login as first user
        return logged_in(session[session.keys()[0]])

@app.route("/login/", methods=["POST"])
def login():
    #login details are submitted through form
    #evaluate them in this function

    authenticate = False
    name = request.form.get("uname")
    pswd = request.form.get("pwd")
    str = "User name %s doesn't exists on this website" % (name)
    #pull login table from database
    #compare it with username
    res = db.execute("select * from users_info;")

    if name in session:
        url = "/user/%s" %name
        return logged_in(session[session.keys()[0]])
    #for each of result rows
    for row in res :
        #match username
        if name == row['uname'] :
            if pswd == row['password'] :
                str = "<h1>Welcome %s <h1>" %(name)
                authenticate = True
                session[name] = name
                url = "/user/%s" %name
                return logged_in(session[name])
                #return "%s logged in" %name
            else :
                str = "You entered a wrong password"
                authenticate = False
                return str

@app.route("/logout/<uname>",methods=["GET"])
def logout(uname):
    if uname in session:
        session.pop(uname,None)
        return "%s is logged out" %uname
    else :
        return "Log in first to log out"

@app.route("/<uname>", methods=["GET"])
def logged_in(uname):
    if uname in session:
        return "logged in as %s" %uname
    else:
        return render_template("login.html")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html",message=" abc")

@app.route("/signup", methods=["POST"])
def signup():
    uname_requested = request.form.get('inputUsername')
    password_requested = request.form.get('inputPassword')
    password_confirmation = request.form.get('inputConfirmPassword')

    if check_for_uname_availablilty(uname_requested):
        #do nothing for now
        if(password_requested == password_confirmation):
            res = create_user(uname_requested, password_requested)
            if res:
                return redirect(url_for("login_page"))
            else:
                return "ERROR"
        else :
            return render_template("signup.html", passwordMatchCheck="Passwords don't match")
    else:
        return render_template("signup.html", userNameCheckMsg="Sorry, this username is taken", userNameCheckMsgStyle="red;")
    return "checking the data sent for %s" %uname_requested

def check_for_uname_availablilty(uname_requested):
    #this function takes a requested user name anc checks
    #if it exists in database or not.
    res = db.execute("select * from users_info;")
    for row in res :
        #check username
        if uname_requested == row['uname'] :
            #username exists
            print("user name already exists")
            return False
    return True

def create_user(uname, password):
    res = db.execute("INSERT INTO users_info (uname, password) VALUES(:uname, :password);",
    {"uname": uname,"password": password})
    print("Create user:{}".format(res))
    db.commit()
    return res
