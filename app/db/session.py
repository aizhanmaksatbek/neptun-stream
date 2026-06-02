from ..config.settings import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker
    )

engine = create_async_engine(DB_URL)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with SessionLocal() as session:
        yield session
