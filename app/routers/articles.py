import uuid
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Query, APIRouter, Depends, status
from typing import Annotated
from ..db.models import Article, ArticleBase
from ..db.session import get_session

router = APIRouter()


@router.get("/articles/")
async def get_home_page(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Article]:
    """This function returns the article ids and titles.

    Returns:
        list[Article]: list of articles
    """
    articles = (
        await session.execute(select(Article).offset(offset).limit(limit))
        ).scalars().all()
    return articles


@router.get("/articles/{article_title}")
async def get_article(
    article_title: str,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> Article:
    """
    This function retrieves the article title and content by its title.

    Parameters:
        article_title (str): title of the article

    Returns:
        Article: article title, content, id
    """

    article = (
        await session.execute(
            select(Article).where(Article.title == article_title)
            )
        ).scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article {article_title} not found"
            )
    return article


@router.post("/articles/")
async def publish_article(
    article: ArticleBase,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:
    """This function saves the article in database using unique id.
    Parameters:
        title (str): title of the article
        content (str): content of the article
    Returns:
        int: unique id of the article from the stored database
    """
    _article: dict = {
        "id": str(uuid.uuid4()),
        "title": article.title,
        "content": article.content
        }

    _article_verified: Article = Article(**_article)
    session.add(_article_verified)
    await session.commit()
    await session.refresh(_article_verified)
    return {
        "message": f"Article with id {_article_verified.id} added successfully"
        }
