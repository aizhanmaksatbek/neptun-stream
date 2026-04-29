from fastapi import FastAPI
from alembic.scripts import create_db_and_tables
from .routers import articles
from .config.settings import sqlite_url, connect_args
from sqlmodel import create_engine


app = FastAPI()
app.include_router(articles.router)


@app.on_event("startup")
def on_startup():
    engine = create_engine(sqlite_url, connect_args=connect_args)
    create_db_and_tables(engine)


