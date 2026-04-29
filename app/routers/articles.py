import uuid
from ..dependencies import SessionDep
from sqlmodel import select
from fastapi import HTTPException, Query, APIRouter
from typing import Annotated
from ..db.base import Article, ArticleBase

router = APIRouter()


@router.get("/articles/")
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


@router.get("/articles/{article_id}")
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


@router.post("/articles/")
def publish_article(
    article: ArticleBase,
    session: SessionDep
) -> dict:
    """This function saves the article in database using unique id.
    Parameters:
        title (str): title of the article
        content (str): content of the article
    Returns:
        int: unique id of the article from the stored database
    """

    id = str(uuid.uuid4())
    print(id)

    _article: Article = Article(id=id, title=article.title, content=article.content)
    session.add(_article)
    session.commit()
    session.refresh(_article)
    return {"message": f"Article with id {_article.id} published successfully"}