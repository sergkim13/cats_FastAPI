import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config_settings.config import (
    TEST_DB_HOST,
    TEST_DB_NAME,
    TEST_DB_PASS,
    TEST_DB_PORT,
    TEST_DB_USER,
)
from src.database.database_settings import get_session
from src.database.models import Base, Cats
from src.main import app

# Test database fixtures
SQLALCHEMY_TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)
CAT_1 = {"name": "Barsik", "color": "black", "tail_length": 12, "whiskers_length": 7}
CAT_1_PATCH = {"color": "red", "tail_length": 11}
CAT_1_UPDATED = {"name": "Barsik", "color": "red", "tail_length": 11, "whiskers_length": 7}
CAT_2 = {"name": "Vasya", "color": "red", "tail_length": 8, "whiskers_length": 3}


# Test database fixtures
@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def create_engine():
    test_engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def test_session(create_engine):
    connection = await create_engine.connect()
    transaction = await connection.begin()
    test_session = AsyncSession(bind=connection)

    yield test_session

    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(test_session):
    app.dependency_overrides[get_session] = lambda: test_session

    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


# CRUD fixtures
@pytest_asyncio.fixture(scope="function")
async def fake_cat(test_session):
    stmt = insert(Cats).values([CAT_1])
    await test_session.execute(stmt)
    await test_session.commit()


@pytest_asyncio.fixture(scope="function")
async def fake_cats(test_session):
    stmt = insert(Cats).values([CAT_1, CAT_2])
    await test_session.execute(stmt)
    await test_session.commit()
