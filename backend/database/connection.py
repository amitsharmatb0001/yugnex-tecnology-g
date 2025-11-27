"""
FILE: connection.py
PATH: yugnex/backend/database/connection.py
PURPOSE: Handles asynchronous database connection and session management.
WORKING:
    1. Creates an async engine using SQLAlchemy and settings.
    2. Defines a session factory (AsyncSessionLocal).
    3. Provides a dependency (get_db) for FastAPI routes.
USAGE:
    @app.get("/")
    async def endpoint(db: AsyncSession = Depends(get_db)):
        ...
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings

# Step 1: Create Async Engine
# This establishes the connection pool to the PostgreSQL database.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True if settings.ENV == "development" else False,
)

# Step 2: Create Session Factory
# This factory generates new session instances for each request.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Step 3: Define Declarative Base
class Base(DeclarativeBase):
    """
    PURPOSE: Base class for all SQLAlchemy ORM models.
    PARAMS: None
    RETURNS: None
    WORKING: Inherits from DeclarativeBase to register models.
    """
    pass

# Step 4: Dependency for Routes
async def get_db():
    """
    PURPOSE: Provides a database session to FastAPI routes.
    PARAMS: None
    RETURNS: AsyncGenerator[AsyncSession, None]
    WORKING:
        1. Creates a new AsyncSession.
        2. Yields the session to the route handler.
        3. Ensures the session is closed after the request completes.
    EXAMPLE:
        async for session in get_db():
            result = await session.execute(...)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()