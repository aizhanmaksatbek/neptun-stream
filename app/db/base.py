from sqlmodel import SQLModel, Field


class ArticleBase(SQLModel):
    title: str = Field(index=True)
    content: str = Field(index=True)


class Article(ArticleBase, table=True):
    id: str | None = Field(default=None, primary_key=True)


class User(SQLModel, table=True):
    username: str = Field(index=True, unique=True, primary_key=True)
    password: str = Field(index=False) # hash of the plain password


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
    scopes: list[str] = []