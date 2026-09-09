import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.database import get_async_session, Base
from app.users.models import User, Scan
from app.wines.models import Wine
from passlib.context import CryptContext
from app.users.dependencies import get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/wine_test"

# УБРАЛИ кастомный event_loop fixture — он deprecated и ломает loop'ы

@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.exec_driver_sql("DROP SCHEMA public CASCADE;")
        await conn.exec_driver_sql("CREATE SCHEMA public;")
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.exec_driver_sql("DROP SCHEMA public CASCADE;")
        await conn.exec_driver_sql("CREATE SCHEMA public;")
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(test_engine):
    session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def test_user(db_session):
    user = User(
        email="test@example.com",
        hashed_password=pwd_context.hash("secret123"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def auth_token(test_user):
    from app.users.auth import create_access_token
    return create_access_token({"sub": str(test_user.id)})

@pytest_asyncio.fixture
async def auth_headers(test_user):
    from app.users.auth import create_access_token
    from app.users.dependencies import get_current_user

    async def override_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_current_user
    token = create_access_token({"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def client(db_session):
    async def override_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()