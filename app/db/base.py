from sqlmodel import SQLModel, Field


class ArticleBase(SQLModel):
    title: str = Field(index=True)
    content: str = Field(index=True)


class Article(ArticleBase, table=True):
    id: str | None = Field(default=None, primary_key=True)
