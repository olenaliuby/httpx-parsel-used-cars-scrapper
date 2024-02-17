from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from database.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, class_=AsyncSession, bind=engine
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
