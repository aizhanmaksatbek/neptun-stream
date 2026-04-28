from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Annotated


class Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)


sqlite_file_name = "database_neptun.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/articles/")
def get_home_page(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Article]:
    """This function returns the article ids and titles.

    Returns:
        list[Article]: list of articles
    """
    articles = session.exec(select(Article).offset(offset).limit(limit)).all()
    return articles


@app.get("/articles/{article_id}")
def get_article(
    article_id: int,
    session: SessionDep
) -> Article:
    """
    This function retrieves the article title and content by its id.

    Parameters:
        article_id (int): id of the article

    Returns:
        Article: article title, content, id
    """

    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article {article_id} not found"
            )
    return article


@app.post("/articles/")
def publish_article(
    article: Article,
    session: SessionDep
) -> Article:
    """This function saves the article in database using unique id.
    Parameters:
        title (str): title of the article
        content (str): content of the article
    Returns:
        int: unique id of the article from the stored database
    """

    session.add(article)
    session.commit()
    session.refresh(article)
    return article
