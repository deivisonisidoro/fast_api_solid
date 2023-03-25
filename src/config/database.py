from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db():
    """
    Create all database tables.

    This function creates all database tables defined in the models.py file, based on the metadata created by the declarative base.

    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get a database session.

    This function returns a context manager that provides a SQLAlchemy session. The session is closed automatically when the context manager is exited.

    Returns:
        generator: A generator that yields a database session.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
