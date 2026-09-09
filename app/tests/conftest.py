import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.database import get_async_session, Base
from app.users.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/wine_test"
CELERY_TASK_ALWAYS_EAGER = True

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


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
async def auth_token(client, test_user):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
