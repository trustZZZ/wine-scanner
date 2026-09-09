from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings

Base = declarative_base()

# Синхронная часть (Celery, Alembic)
engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sync_db():
    return SessionLocal()

# Асинхронная часть (FastAPI)
async_engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
