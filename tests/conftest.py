import os

from dotenv import load_dotenv

import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.pool import NullPool

from app.database.db import Base, get_db
from app.main import app


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

test_engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=True
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client_db(setup_database):
    """
    Упрощенная версия без сложных генераторов.
    """

    async with test_engine.connect() as conn:
        transaction = await conn.begin()
        test_session = async_sessionmaker(bind=conn, class_=AsyncSession)()

        def override_get_db():
            return test_session

        app.dependency_overrides[get_db] = override_get_db

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
        ) as client:
            client.test_data = {
                'name': 'new_task',
                'description': 'new_description',
                'status': 'Создано'
            }
            yield client

        await test_session.close()
        await transaction.rollback()

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db_session(setup_database):
    """Фикстура для тестирования моделей с чистой сессией"""

    async with test_engine.connect() as conn:
        transaction = await conn.begin()
        test_session = async_sessionmaker(bind=conn, class_=AsyncSession)()

        try:
            yield test_session
        finally:
            await transaction.rollback()
            await test_session.close()


@pytest_asyncio.fixture
async def update_data():
    update_data = {
        'name': 'update_task',
        'description': 'update_description',
        'status': 'В работе'
    }
    return update_data
