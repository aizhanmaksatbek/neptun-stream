from fastapi import APIRouter
from ..dependencies import SessionDep
from ..db.base import User
from sqlmodel import select


router = APIRouter()


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
def authenticate_user(
    user: User,
    session: SessionDep
):
    db_user = session.get(User, user.username)
    if not db_user:
        return {"error": "Invalid username or password"}
    
    return {"token": f"fake-token-for-user-{user.username}"}