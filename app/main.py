from .routers import articles, users
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()
app.include_router(articles.router)
app.include_router(users.router)

templates = Jinja2Templates(directory="app/frontend/templates")
app.mount(
    "/static",
    StaticFiles(directory="app/frontend/static"),
    name="static"
    )


@app.get("/", include_in_schema=False)
def home(request: Request):
    articles = requests.get("http://localhost:8000/articles/").json()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"articles": articles, "title": "Blog Posts Home"}
        )
