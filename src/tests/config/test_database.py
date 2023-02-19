from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.config.database import create_db, get_db


class TestDatabase:
    def test_create_db(self):
        create_db()

    def test_get_db_returns_db_session(self, monkeypatch):
        mock_session = MagicMock(spec=Session)
        mock_sessionmaker = MagicMock(return_value=mock_session)
        monkeypatch.setattr("src.config.database.SessionLocal", mock_sessionmaker)

        with get_db() as db:
            assert isinstance(db, Session)
