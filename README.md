# neptun-stream
Blog for posting articles.
The system is written using the FastAPI, SQLmodel, Python 3.10.\
It consists a User login by authentication and authorization.
Passwords are encrypted using pwdlib[argon2].\
Token is codified using JWT.

# Endpoints:
- /articles
- /users
- /token

# Database:
Database configuration are in config/settings file.
```
sqlite_file_name = "database_neptun.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
```


# Manual for Running the Application
Create your virtual environment:
bash
```
python -m venv .venv_neptun
source .venv_neptun/bin/activate
deactivate
```

Run the application by
bash
```
fastapi dev app/main.py
or
fastapi dev
```
