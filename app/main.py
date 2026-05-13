from .routers import articles, users
from .config.settings import sqlite_url, connect_args
from .alembic.scripts import create_db_and_tables
from sqlmodel import create_engine
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine(sqlite_url, connect_args=connect_args)
    create_db_and_tables(engine)
    yield
    engine.clear()

app = FastAPI(lifespan=lifespan)
app.include_router(articles.router)
app.include_router(users.router)
