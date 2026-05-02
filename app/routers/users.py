from typing import Annotated
import logging

from pwdlib.exceptions import UnknownHashError
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash

from ..db.base import User
from ..db.session import get_session

logging.basicConfig(level=logging.INFO)

password_hash = PasswordHash.recommended()

def encrypt_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, encrypted_password: str) -> bool:
    try:
        return password_hash.verify(plain_password, encrypted_password)
    except UnknownHashError:
        logging.error("Unknown hash error occurred while verifying password.")
        raise HTTPException(status_code=400, detail="Invalid password.")


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users/")
def get_users(
    session: Annotated[Session, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    """This endpoint gets the users from the Users table in offset and limit range."""
    return session.exec(select(User).offset(offset).limit(limit)).all()

@router.post("/users/")
def add_user(
    user: User,
    session: Annotated[Session, Depends(get_session)]
):
    """This function allows to add a new user to database. It encrypts the password before saving it."""
    user.password = encrypt_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)

@router.delete("/users/{username}")
def delete_user(
    username: str,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()

def decode_fake_token(token: str) -> User:
    return User(username= token + "1", password="encrypted-1")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    return decode_fake_token(token)

@router.get("/users/me")
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

def authenticate_user(
        session: Session,
        username: str,
        password: str
) -> User:
    login_exception = HTTPException(status_code=400, detail="Incorrect username or password")
    user = session.get(User, username)
    if not user:
        raise login_exception
    if not verify_password(password, user.password):
        raise login_exception
    return user

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    """This function logins user and returns a user token."""
    user = authenticate_user(session, form_data.username, form_data.password)
    return {"access_token": user.username, "token_type": "bearer"}
