'''
Jayden Zhang, Margie Cao, Danny Huang, Suhana Kumar
H1N1
SoftDev
P02 - Instabook
Time Spent:
Target Ship Date: 2025-01-15
'''

import os
import time
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import db_helpers as db
import requests
import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

##image configuration
upload_folder = 'static/images'
allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
app.config['upload_folder'] = upload_folder

keys = ["key_goFile.txt", "key_googleFirebase.txt"]
for i in range(len(keys)):
    file = open("app/keys/" + keys[i], "r")
    content = file.read()
    if content: ##if file isnt empty
        keys[i] = content.replace("\n", "")
    file.close()

@app.route('/get-key')
def get_key():
    return send_from_directory('keys', 'key_googleFirebase.txt', as_attachment=False)

def key_check():
    for i in range(len(keys)):
        if ".txt" in keys[i]:
            print(f"api key is missing in {keys[i]}")
        ##check invalid keys

def signed_in():
    return 'username' in session.keys() and session['username'] is not None

def check_user(username):
    user = db.getUser(username)
    print(user)
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
        session["userID"] = db.getId(request.form.get("username"))
        session["photo"] = db.getPhoto(session["username"])
        return redirect('/')
    return render_template("signIn.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.pop("password", None)
    session.pop("name", None)
    session.pop("profilepic", None)
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
            session["photo"] = db.getPhoto(session["username"])
            return redirect('/login')
        else:
            return render_template('signUp.html', message="Username already exists")
    return render_template('signUp.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    if not signed_in():
        return redirect(url_for('login'))
    allUsers = db.getAllUsers()
    users = [
        {
            "name" : user[0],
            "profilePic": url_for('static', filename=f'images/{user[0]}'),
            "profileUrl": url_for('profile', username=user[0])
            }
        for user in allUsers
    ]
    if request.method == 'POST':
        return {"users": users}
    return render_template('search.html', users = users)
                          
                          
@app.route("/reels", methods=['GET', 'POST'])
def reels():
    videos = db.getVideos()  # useful for userID of associated video
    listofUrls = []

    if videos:
        folder_url = videos[0][0]  # first element contains the shared folder URL
        print(f"Scraping folder: {folder_url}")

        # Configure Selenium WebDriver as per documentation
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        DOWNLOAD_DIRECTORY = os.path.abspath("app/static/videos") # static/videos will be our download directory
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_DIRECTORY, 
            "download.prompt_for_download": False,  
            "download.directory_upgrade": True,  
            "safebrowsing.enabled": True,  
        })
        
        # HAVE TO CHANGE THIS TO WHICHEVER COMPUTER YOUR USING :SOB:
        info = platform.platform()
        service = ''
        
        if 'mac' in info:
            if 'arm64' in info:
                service = Service('app/selenium/chromedriver-mac-arm64/chromedriver')
            else:
                service = Service('app/selenium/chromedriver-mac-x64/chromedriver')
        elif 'win' in info:
            if '32' in info:
                service = Service('app/selenium/chromedriver-win32/chromedriver')
            else:
                service = Service('app/selenium/chromedriver-win64/chromedriver')
        else:
            service = Service('app/selenium/chromedriver-linux64/chromedriver')
            
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(folder_url) # get the folder into the chrome driver

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body")) # wait for the driver to find the "body" tag
            )

            print("Finished Finding the Body Tag.")

            play_buttons = WebDriverWait(driver, 20).until( # all videos in GoFile have a button with the class "item-play" to play the video
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'item_play')]"))
            )

            close_buttons = WebDriverWait(driver, 20).until( # all videos in GoFile have a button with the class "item-close" to close the video
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'item_close')]"))
            )

            print("Finished Checking Buttons.")

            print(f"Found {len(play_buttons)} play buttons")
            print(f"Found {len(close_buttons)} close buttons")

            for index, button in enumerate(play_buttons): # enumerate allows me to access index
                try:
                    print(f"Clicking Play button {index + 1}")
                    button.click()  # click the button to play the video
                    
                    video = WebDriverWait(driver, 20).until( # finds a video tag
                        EC.presence_of_element_located((By.TAG_NAME, "video"))
                    )

                    source = video.find_element(By.TAG_NAME, "source") # finds the source tag in the video tag
                    video_src = source.get_attribute("src") # finds the src attribute in the source tag

                    if video_src: # if it's present, it adds the url to a list
                        listofUrls.append(video_src)
                        print(f"Extracted video src: {video_src}")
                    
                    close_buttons[index].click() # presses the close button to repeat for the next play button
                except Exception as e:
                    print(f"Error handling Play button {index + 1}: {e}")
                    continue
            
            newListOfUrls = [] # list where the downloads of the urls are stored
            
            for index, url in enumerate(listofUrls):
                print(f"Processing URL {index + 1}/{len(listofUrls)}: {url}")

                video_filename = f"video_{index + 1}.mp4" # renames the video to an index to differentiate them
                newListOfUrls.append(video_filename) # appends it to the new url list

                if video_filename in os.listdir(DOWNLOAD_DIRECTORY): # if the video already in the directory, it skips this iteration to save memory and stops the download.
                    print(f"File {video_filename} already exists. Skipping download.")
                    continue 
                else:
                    driver.get(url)  # opens the download link in the chrome driver which downloads the link IF it's not ALREADY present
                    time.sleep(5)  # gives time before the download starts.

                    downloaded_files = os.listdir(DOWNLOAD_DIRECTORY) # finds the downloaded file
                    if downloaded_files:
                        latest_file = max([os.path.join(DOWNLOAD_DIRECTORY, f) for f in downloaded_files], key=os.path.getctime) # finds the most recent file via time downloaded

                        video_path = os.path.join(DOWNLOAD_DIRECTORY, video_filename) # attaches the video the static/video directory
                        os.rename(latest_file, video_path) # renames the latest file to match the video_{index}.mp4 in the downloaded files list
                        print(f"Renamed {latest_file} to {video_path}")
                    else:
                        print(f"No files downloaded for {url}")

            listOfUploaders = []
            for video in videos:
                listOfUploaders.append(video[1])
            combined_videos = list(zip(newListOfUrls, listOfUploaders))
        finally:
            driver.quit()  # exits the driver
        print(newListOfUrls) # debugging statement
    return render_template("reels.html", combined_videos=combined_videos)

@app.route('/upload', methods=['GET', 'POST'])
def uploadReels():
    response = requests.get("https://api.gofile.io/servers")
    data = response.json()
    if data['status'] == 'ok':
        serverLink = f"https://{data['data']['servers'][0]['name']}.gofile.io"       

    video = request.files['video']
    headers = {'Authorization': f'Bearer {keys[0]}'}
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

@app.route("/profile/<username>/edit", methods=['GET', 'POST'])
def profile(username):
    if not signed_in():
        return redirect(url_for('login'))
    
    if session["username"] != username:
        return render_template('profile.html', message="No Access! >:(")
    
    if request.method == 'POST':
        profile = request.files['file']
        if profile:
            original = profile.filename
            if '.' in original:
                fileExtension = original.rsplit('.', 1)[1].lower()  # grabs the extension
            else:
                return render_template('profile.html', message="No file extension found.")
        
            imageExtensions = {'jpg', 'jpeg', 'png', 'gif', 'heic', 'bmp', 'webp'}
            if fileExtension not in imageExtensions:
                return render_template('profile.html', message="Invalid file type. Only image files are allowed.")
            
            filename = f"{session['username']}.{fileExtension}"
            filePath = os.path.join("app/static/images", filename)
            profile.save(filePath)
            db.saveImageToDB(session["username"], filePath)
            session['photo'] = filePath
    
    userPhoto = db.getPhoto(username)
    if userPhoto:
        updatedLink = url_for('static', filename=userPhoto[0].replace('app/static/', ''))
    print(updatedLink)
    return render_template("profile.html", name = session["username"], profile = updatedLink, editable = True)

@app.route("/profile/<username>", methods=['GET'])
def view_profile(username):
    userPhoto = db.getPhoto(username)
    if not userPhoto:
        return render_template('profile.html', message="Profile Not Found.")
    
    updatedLink = userPhoto[0].replace("app/static/", "../static/")
    return render_template("profile.html", name = username, profile = updatedLink, editable = False)

@app.route("/messages", methods=['GET', 'POST'])
def messages():
    if not signed_in():
        return redirect(url_for('login'))
    allUsers = db.getAllUsers()
    userlist = []
    for users in allUsers:
        userlist.append(users[0])
    return render_template('messages.html', people=userlist, user=session['username'])

if __name__ == "__main__":
    app.debug = True
    app.run()
