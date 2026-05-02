import uuid
from sqlmodel import select, Session
from fastapi import HTTPException, Query, APIRouter, Depends
from typing import Annotated
from ..db.base import Article, ArticleBase
from ..db.session import get_session

router = APIRouter()


@router.get("/articles/")
def get_home_page(
    session: Annotated[Session, Depends(get_session)],
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
    session: Annotated[Session, Depends(get_session)]
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
    session: Annotated[Session, Depends(get_session)]
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