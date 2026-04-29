from ..config.settings import sqlite_url, connect_args
from sqlmodel import create_engine, Session


def get_session():
    engine = create_engine(sqlite_url, connect_args=connect_args)
    with Session(engine) as session:
        yield session