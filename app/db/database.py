# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False, #  If set to True, it starts a new transaction automatically after a commit.
    autoflush=True, #  If True, all query operations will issue a flush call to the session before proceeding.
    # bind=None, #  You can specify a specific engine to bind to if you're using multiple databases.
    future=True, #  Enables SQLAlchemy 2.0 behavior in 1.4. This is typically set to True for newer applications.
    twophase=False # If True, enables two-phase transaction support.
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()