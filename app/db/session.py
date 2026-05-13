from ..config.settings import sqlite_url, connect_args
from sqlmodel import create_engine, Session

engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session
