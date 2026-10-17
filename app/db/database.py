from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    )

SessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session