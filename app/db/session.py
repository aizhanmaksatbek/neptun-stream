from ..config.settings import DB_URL
from sqlmodel import create_engine, Session
from sqlmodel import SQLModel
from typing import Any

engine = create_engine(DB_URL)


def create_db_and_tables(engine: Any) -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
