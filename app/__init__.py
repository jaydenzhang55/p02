'''
Jayden Zhang, Margie Cao, Danny Huang, Suhana Kumar
H1N1
SoftDev
P02 - Instabook
Time Spent:
Target Ship Date: 2025-01-15
'''

import os
import random
import urllib.request
import json
from flask import Flask, render_template, request, redirect, url_for, session
import db_helpers as db
import sqlite3

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

keys = ["key_goFile.txt", "key_googleFireBase.txt"]
for i in range(len(keys)):
    file = open("app/keys/" + keys[i], "r")
    content = file.read()
    if content: ##if file isnt empty
        keys[i] = content.replace("\n", "")
    file.close()

def key_check():
    for i in range(len(keys)):
        if ".txt" in keys[i]:
            print(f"api key is missing in {keys[i]}")
        ##check invalid keys

def signed_in():
    return 'username' in session.keys() and session['username'] is not None

def check_user(username):
    user = db.getUser(username)
    if user is None:
        return False
    return user[0] == username

def check_password(username, password):
    user = db.getHash(username)
    if user is None:
        return False
    print(user)
    return user[0] == password

@app.route("/")
def home():
    if session.get("username") != None:
        return render_template("homePage.html", name = session["name"])
    return redirect(url_for("signup"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if signed_in():
        return redirect('/')
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pw')
        if not check_user(username):
            return render_template("signIn.html", message="No such username exists")
        if not check_password(username, password):
            return render_template("signIn.html", message="Incorrect password")
        session['username'] = username
        session["name"] = db.getName(session['username'])[0]
        session["password"] = request.form.get("pw")
        return redirect('/')
    return render_template("signIn.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.pop("password", None)
    session.pop("name", None)
    return redirect(url_for("home"))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if signed_in():
        return redirect('/')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['pw']
        name = request.form['name']
        user = db.getUser(username)
        if user is None:
            db.addUser(name, username, password)
            session["name"] = name
            session["username"] = username
            session["password"] = password
            return redirect('/login')
        else:
            return render_template('signUp.html', message="Username already exists")
    return render_template('signUp.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    return

@app.route("/reels", methods=['GET', 'POST'])
def reels():
    return

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    return

@app.route("/messages", methods=['GET', 'POST'])
def messages():
    if not signed_in():
        return redirect(url_for('login'))
    allUsers = db.getAllUsers()
    userlist = []
    for users in allUsers:
        userlist.append(users[0])
    return render_template('messages.html', people=userlist)

if __name__ == "__main__":
    app.debug = True
    app.run()