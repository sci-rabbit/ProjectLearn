from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.models import Base
from settings import REAL_DATABASE_URL

engine = create_async_engine(REAL_DATABASE_URL)
async_db_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session():
    async with async_db_session() as session:
        yield session


async def setup_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)