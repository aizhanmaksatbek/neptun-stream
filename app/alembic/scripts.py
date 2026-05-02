from sqlmodel import SQLModel
from typing import Any


def create_db_and_tables(engine: Any) -> None:
    SQLModel.metadata.create_all(engine)