from .routers import articles, users
from fastapi import FastAPI


app = FastAPI()
app.include_router(articles.router)
app.include_router(users.router)
