from enum import unique
from tkinter import PanedWindow
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv   # pip install python-dotenv for using .env file for storing environment variables
load_dotenv()
from flask_login import UserMixin


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"]=os.environ.get("SECRET_KEY")
db = SQLAlchemy(app)

class User(db.Model):
    '''
    User table for storing the username and hash of password
    '''
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20),unique= True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    '''
    Post table for storing the post of the user
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# @app.route("/")
# def hello_world():
#     print("Hello World")
#     return "Hello World"

# @app.route("/login")
# def hello():
#     return render_template("login.html")



@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(userid = username).first()
        if user.userid==username and user.check_password(password):
            return redirect(url_for("dashboard", username=user.userid))
        else:
            return render_template("login.html")
    elif request.method=="GET":
        return render_template("login.html")

@app.route("/register", methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(userid = username).first()
    if user:
        return render_template("login.html", error="User already exists!")
    else:
        new_user = User(userid=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for("login"))


# @app.route("/register", method=['GET','POST'])
# def register():
#     #get the info from the form

#     #chck the user information

#     #save the information
#     pass

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)