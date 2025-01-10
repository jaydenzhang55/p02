import os
import random
import urllib.request
import json
from flask import Flask, render_template, request, redirect, url_for, session
import db_helpers as db

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

@app.route("/")
def home():
    if session.get("username") != None:
        return render_template("homePage.html", name = session["name"])
    return redirect(url_for("signup"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if (session.get('username') == None):
       return redirect(url_for("signup"))
    try:
        if request.method == "POST" and db.validateUser(request.form.get("username"), request.form.get("pw")):
            session["username"] = request.form.get("username")
            session["name"] = db.getName(session["username"])
            session["password"] = request.form.get("pw")
            print('success')
            return render_template("homePage.html")
    except:
        print("yapper")
        return render_template("signUp.html")
    return render_template("signIn.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.pop("password", None)
    session.pop("name", None)
    return redirect(url_for("home"))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("pw")

        print(f"Name: {name}, Username: {username}, Password: {password}")  # Debugging output

        if name and username and password:
            print(f"Name: {name}, Username: {username}, Password: {password}")  # Debugging output
            session["name"] = name
            session["username"] = username
            session["password"] = password
            db.addUser(name, username, password)
            return redirect(url_for("login"))
    return render_template("signUp.html")

if __name__ == "__main__":
    app.debug = True
    app.run()