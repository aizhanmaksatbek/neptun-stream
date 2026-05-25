from pathlib import Path


DB_PATH = str((Path().parent / 'db.sqlite').resolve())
sqlite_url = f"sqlite:///{DB_PATH}"

connect_args = {"check_same_thread": False}

# Token
# openssl rand -hex 32
SECRET_KEY = "6ccc15a0faae55a8a5d44c35fa9c3a5d54fae8d91ea8902c0df80b57ba60e6e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
