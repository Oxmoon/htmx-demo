# htmx-demo

## Installation

If you have python3 installed but not virtualenv, you can install it with: `python3 -m pip install --user virtualenv`

### First time setup

While in your htmx-demo directory run these commands:

```
python3 -m venv .venv
. .venv/bin/activate
pip install -r ./requirements.txt
```

Also ensure sqlite3 is downloaded on your system.
To initialize the database run these commands:

```
flask shell
db.create_all()
# exit with: quit()
```

### To run the local development server

Ensure your virtual enviornement is running with: `. .venv/bin/activate`  
Then run `flask --app app run` to start the server.

### To run on school server

Ensure your virtual enviornement is running with: `. .venv/bin/activate`  
Ensure gunicron is installed with `pip install gunicorn`  
Then run `gunicorn app:app -w 4 -b:{YOUR PORT# HERE}` to start the server.
