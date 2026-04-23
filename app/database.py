from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models import Base


class DatabaseConfig(BaseSettings):
    DATABASE_URL: str


db_config = DatabaseConfig()  # ty:ignore[missing-argument]
engine = create_async_engine(db_config.DATABASE_URL)
async_session = async_sessionmaker(engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
