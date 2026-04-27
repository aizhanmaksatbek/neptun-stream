from fastapi import FastAPI
import random


app = FastAPI()


@app.get("/articles/")
def get_home_page() -> dict:
    """This function returns the article ids and titles.

    Returns:
        dict: home page content
    """
    return {random.randint(1, 1000): "title"}


@app.get("/articles/{article_id}")
def get_article(article_id: int) -> dict:
    """
    This function retrieves the article title and content by its id.

    Parameters:
        article_id (int): id of the article

    Returns:
        dict: article title, content, id
    """

    return {
        "title": "title",
        "content": "content",
        "article_id": article_id
        }


@app.post("/articles/")
def publish_article(title: str, content: str) -> int:
    """This function saves the article in database using unique id.
    Parameters:
        title (str): title of the article
        content (str): content of the article
    Returns:
        int: unique id of the article from the stored database
    """

    return random.randint(1, 1000)
