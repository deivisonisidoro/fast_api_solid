import os
import sys
from contextlib import contextmanager
from typing import Any, Generator

import pytest
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.routers import router

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import from db,main.py

faker = Faker()


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(router, prefix="/api")
    return app


@contextmanager
@pytest.fixture
def db():
    session = SessionTesting()

    Base.metadata.create_all(bind=engine)

    yield session

    session.rollback()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()  # close all connections to the database

    try:
        os.remove("test.db")
    except FileNotFoundError:
        pass


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def client(app: FastAPI, db: SessionTesting) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def user_data():
    """
    Generate a random user data for testing.
    """
    return {
        "name": faker.name(),
        "email": faker.email(),
        "password": faker.password(),
    }


class TestDB:
    @classmethod
    def setup_class(cls):
        Base.metadata.create_all(bind=engine)
        cls.Session = sessionmaker(bind=engine)

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(bind=engine)
