import sqlite3, requests, os
from flask import session
import bcrypt

#Create SQLite Table, creates if not already made
DB_FILE = os.path.join(os.path.dirname(__file__), "../database.db")

db = sqlite3.connect(DB_FILE)
cur = db.cursor()


cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    profilepic BLOB
);
''')
db.commit()
db.close()

# User Helpers


def userTable():
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, photo BLOB NOT NULL)")
    db.commit()

def videoTable():
    cur.execute("CREATE TABLE videos(id INTEGER PRIMARY KEY, userId INTEGER, videoUrl TEXT)")
    db.commit()

def addUser(name, username, password):
    try:
        with open("./static/images/default.svg", "rb") as file:
            default = file.read()
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute("INSERT INTO users (name, username, password, photo) VALUES (?, ?, ?, ?)", (name, username, password, default))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        db.commit()
        db.close()

def removeUser(id):
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute(f"DELETE FROM users WHERE id='{id}'")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        db.commit()
        db.close()
    

def validateUser(username, password):
    dbPassword = getHash(username)
    if dbPassword:
        return validatePassword(dbPassword, password)
    return False

def getUser(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        user = cur.execute(f"SELECT username FROM users WHERE username='{username}'").fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        user = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return user

def getName(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        name = cur.execute(f"SELECT name FROM users WHERE username='{username}'").fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        name = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return name

def getId(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        Id =  cur.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        Id = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return Id

def getHash(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        Hash = cur.execute(f"SELECT password FROM users WHERE username='{username}'").fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        Hash = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return Hash

def getAllPhotos():
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        photos = cur.execute("SELECT profilepic FROM users").fetchall()
    except sqlite2.Error as e:
        print(f"An error occurred: {e}")
        photos = None
    finally:
        cur.close()
        db.commit()
        db.close()
    return photos

def getPhoto(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    photo =  cur.execute(f"SELECT profilepic FROM user WHERE username='{username}'").fetchone()[0]
    finally: 
         cur.close()
         db.commit()
         db.close()
    return photo

# Function to save an image to the database
def save_image_to_db(username, image_path):
    with open(image_path, 'rb') as file:
        bdata = file.read()
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute(f"UPDATE users SET profile_picture = ? WHERE username = ?",(bdata, username))
    db.commit()
    db.close()


def getAllUsers():
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        users = cur.execute("SELECT username FROM users").fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        users = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return users


#error?
def hashPassword(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(bytes, salt)
    return hashedPassword

def validatePassword(hash, password):
    print("Password: " + password)
    print("Matches Hash: " + str(bcrypt.checkpw(password.encode("utf-8"), hash)))
    return bcrypt.checkpw(password.encode("utf-8"), hash)

def uploadVideo(userID, gofileURL):
    db = sqlite3.connect(DB_FILE)    
    cur = db.cursor()
    cur.execute("INSERT INTO videos (userId, videoUrl) VALUES (?, ?)", (userID, gofileURL))
    db.commit()

def getVideos():
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("SELECT videos.videoUrl, users.name FROM videos JOIN users ON videos.userId = users.id")
    reels = cur.fetchall()
    return reels

#userTable()
#videoTable()
