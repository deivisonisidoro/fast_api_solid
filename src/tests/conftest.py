import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.database import Base


@pytest.fixture
def db():
    engine = create_engine("sqlite:///test.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(bind=engine)

    yield session

    session.rollback()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()  # close all connections to the database

    try:
        os.remove("test.db")
    except FileNotFoundError:
        pass


class TestDB:
    @classmethod
    def setup_class(cls):
        engine = create_engine("sqlite:///test.db", echo=True)
        Base.metadata.create_all(bind=engine)
        cls.Session = sessionmaker(bind=engine)

    @classmethod
    def teardown_class(cls):
        engine = create_engine("sqlite:///test.db", echo=True)
        Base.metadata.drop_all(bind=engine)
