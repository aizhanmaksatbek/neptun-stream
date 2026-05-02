from .routers import articles, users
from .config.settings import sqlite_url, connect_args
from .alembic.scripts import create_db_and_tables
from sqlmodel import create_engine
from fastapi import FastAPI

import uvicorn


app = FastAPI()
app.include_router(articles.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    engine = create_engine(sqlite_url, connect_args=connect_args)
    create_db_and_tables(engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
