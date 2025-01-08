## InstaBook By H1N1

## Team Members Roles:
- **Jayden Zhang (PM)**: 
- **Margie Cao**: User Authentication, Functions/Search Bar, Front-end (HTML)
- **Danny Huang**: Setting up Python, SQLite3, and Tailwind environments, Watchlists, Front-end (CSS + Tailwind)
- **Suhana Kumar**: Setting up Python, SQLite3, and Tailwind environments, Watchlists, Front-end (CSS + Tailwind)
## Description:

### A Social Media Platform

Users can:
- Log in and log out into their accounts
- View the reels of other users
- Post their own reels
- Search for other users
- Friend other users
- Message other users


## Install guide:
### 1) Clone the required directory to run the program:
```  
    $git clone git@github.com:jaydenzhang55/p02.git
```
### 2) Set up a virtual environment 
```
    $python3 -m venv foo
```
### 3) Activate virtual environment
```
    $source ../foo/bin/activate
```
### 4) Move into directory
```
   $cd p02
```
### 5) Install the required packages
```
    $pip install -r requirements.txt
```
### 6) Acquire your API Keys
```
    - Navigate to reademe.md and follow the links within to acquire API keys
    - Place your API keys into key_<API Name>.txt for each API locally.
    - Run command below to keep your API from being pushed to github:
        git update-index --skip-worktree <path-name>
```
## Launch Code:

### 1) Make a Python virtual environment 
```
      a. Open up your device's terminal

      b. Type ```$ python3 -m venv {path name}``` or ```$ py -m venv {path name}```

      c. Type in one of the commands into your terminal for your specific OS to activate the environment

      - Linux: ```$ . {path name}/bin/activate```
    
      - Windows Command Prompt: ```> {path name}\Scripts\activate```

      - Windows PowerShell: ```> . .\{path name}\Scripts\activate```

      - MacOS: ```$ source {path name}/bin/activate```

      (If successful, the command line should display the name of your virtual environment: ```({path name})$ ```)

      d. When done, type ```$ deactivate``` to deactivate the virtual environment
```

### 2) Move into directory
```
   $cd p02
```
### 3) Launch the app
```   
   $python3 app/__init__.py
```
### 4) Go to local host, copy link below and paste into your browser
```
   http://127.0.0.1:5000
```
