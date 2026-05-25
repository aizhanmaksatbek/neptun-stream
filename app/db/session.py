from ..config.settings import sqlite_url, connect_args
from sqlmodel import create_engine, Session
from sqlmodel import SQLModel
from typing import Any

engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables(engine: Any) -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
