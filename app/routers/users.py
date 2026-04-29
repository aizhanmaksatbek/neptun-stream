from fastapi import APIRouter, Depends
from ..dependencies import SessionDep
from ..db.base import User
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


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
        return {"error": "Invalid username or password"}

    return {"token": f"fake-token-for-user-{token}"}