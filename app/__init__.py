import os
import random
import urllib.request
import json
from flask import Flask, render_template, request, redirect, url_for, session
import db_helpers as db
import requests

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
            session["userID"] = db.getId(request.form.get("username"))
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

@app.route("/search", methods=['GET', 'POST'])
def search():
    return

@app.route("/reels", methods=['GET', 'POST'])
def reels():
    videos = db.getVideos()
    print(videos)

    return render_template("reels.html", videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def uploadReels():
    response = requests.get("https://api.gofile.io/servers")
    data = response.json()
    if data['status'] == 'ok':
        serverLink = f"https://{data['data']['servers'][0]['name']}.gofile.io"       

    video = request.files['video']
    headers = {'Authorization': 'Bearer t2dUKihjfIfgUSp9u0naxtRR9KmhroXW'}
    folderID={'folderId': "734bfa21-03ba-4763-a0ce-82276b74fb7b"}
    print(serverLink)

    url = f"{serverLink}/uploadFile"
    response = requests.post(url, files={'file': video}, verify=False, data=folderID, headers=headers)
        
    gofile_data = response.json()

    if gofile_data['status'] == 'ok':
        gofileUrl = gofile_data['data']['downloadPage']
        db.uploadVideo(session.get("userID"), gofileUrl)
        print(db.getVideos())
        return redirect(url_for("reels"))
    return "something went wrong pls try again later" 



@app.route("/profile", methods=['GET', 'POST'])
def profile():
    return

@app.route("/messages", methods=['GET', 'POST'])
def messages():
    return

if __name__ == "__main__":
    app.debug = True
    app.run()