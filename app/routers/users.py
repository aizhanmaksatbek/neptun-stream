from typing import Annotated
import logging
from datetime import datetime, timedelta, timezone
from pwdlib.exceptions import UnknownHashError
from sqlmodel import Session, select
from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes
    )
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from ..db.base import User, Token, TokenData
from ..config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
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
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."}
    )

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


def get_user_by_username(
    session: Session,
    username: str
) -> User | None:
    return session.exec(select(User).where(User.username == username)).first()


def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)],

) -> User:
    logging.info(f"{security_scopes.scopes}")
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope = {security_scopes.scope_str}"
    else:
        authenticate_value = "Bearer"
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        if username is None:
            raise credentials_exception
        scopes = payload.get("scope", "")
        token_scopes = scopes.split(" ")
        token_data = TokenData(username=username, scopes=token_scopes)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user_by_username(session, username=username)
    if user is None:
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough credentials",
                headers={"WWW-Authenticate": authenticate_value}
                )
    return user

def get_current_active_user(
        current_user: Annotated[User, Security(get_current_user, scopes=["me"])]
):
    return current_user

@router.get("/users/me")
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.get("/users/me/items")
def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])]
) -> dict:
    return {"item_id": "Foo", "owner": f"{current_user.username}"}

def authenticate(
        session: Session,
        username: str,
        password: str
) -> User | bool:
    user = session.get(User, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """This function encodes the user information in a JWT token.
    Parameters:
    data (dict): A dictionary containing the user information to be encoded in the token.
    - data: dictionary with username key, value
    - expires_delta: expiration timedelta in minutes

    Returns:
    - jwt token
    """
    data_copy = data.copy()
    if expires_delta:
        expire_date = datetime.now(timezone.utc) + expires_delta
    else:
        expire_date = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_copy.update({"exp": expire_date})
    encoded_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
) -> Token:
    """This function logins user and returns a user token."""
    user = authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_token(
        data={"sub": user.username, "scope":" ".join(form_data.scopes)},
        expires_delta=expires_delta
    )
    return Token(access_token=token, token_type="bearer")
