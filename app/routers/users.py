from typing import Annotated

from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..db.base import User
from ..db.session import get_session
import logging

logging.basicConfig(level=logging.INFO)

def encrypt_password(password: str) -> str:
    return f"encrypted-{password}"


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

def decode_fake_token(token: str) -> User:
    return User(username= token + "1", password="encrypted-1")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    return decode_fake_token(token)

@router.get("/users/me")
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    """This function logins user and returns a user token."""
    login_exception = HTTPException(status_code=400, detail="Incorrect username or password")
    user = session.get(User, form_data.username)
    if not user:
        raise login_exception
    if user.password != encrypt_password(form_data.password):
        raise login_exception
    return {"access_token": user.username, "token_type": "bearer"}
