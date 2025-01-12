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
);
''')
db.commit()
db.close()

# User Helpers

def addUser(name, username, password):
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))
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

def getPhoto(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        photo =  cur.execute(f"SELECT photo FROM users WHERE username='{username}'").fetchone()[0]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        photo = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return photo

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

# userTable()