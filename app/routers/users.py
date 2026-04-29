from fastapi import APIRouter, Depends
from ..dependencies import SessionDep
from ..db.base import User
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import HTTPException


def encrypt_password(password: str) -> str:
    return f"encrypted-{password}"


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users/")
def get_users(
    session: SessionDep
):
    return session.exec(select(User)).all()


@router.post("/users/")
def add_user(
    user: User,
    session: SessionDep
):
    user.password = encrypt_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)




@router.post("/users/authenticate/")
async def authenticate_user(
    user: User,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    db_user = session.get(User, user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username")
    if db_user.password != encrypt_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"access_token": f"fake-token-for-user-{user.username}", "token_type": "bearer"}
