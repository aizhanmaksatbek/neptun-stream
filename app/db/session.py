from ..config.settings import DB_URL
from sqlmodel import create_engine, Session


engine = create_engine(DB_URL)


def get_session():
    with Session(engine) as session:
        yield session
