import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from ..database import models


@pytest.fixture(scope="module")
def engine():
    db_url = "sqlite:///test.db"
    engine = create_engine(db_url)
    models.metadata.create_all(engine)
    yield engine
    models.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def session(engine):
    SessionLocal = models.sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def bookmark(session):
    bookmark = models.Bookmark(
        title="Test bookmark",
        url="https://testbookmark.com",
        notes="Test notes",
        date_added="2022-03-19 00:00:00",
        date_edited="2022-03-19 00:00:00",
    )
    session.add(bookmark)
    session.commit()
    return bookmark


def test_create_bookmark(bookmark):
    assert bookmark.id is not None
    assert bookmark.title == "Test bookmark"
    assert bookmark.url == "https://testbookmark.com"
    assert bookmark.notes == "Test notes"
    assert bookmark.date_added == "2022-03-19 00:00:00"
    assert bookmark.date_edited == "2022-03-19 00:00:00"


def test_read_bookmark(session, bookmark):
    result = session.execute(select(models.Bookmark)).all()
    assert len(result) == 1
    assert result[0]["title"] == "Test bookmark"
    assert result[0]["url"] == "https://testbookmark.com"
    assert result[0]["notes"] == "Test notes"
    assert result[0]["date_added"] == "2022-03-19 00:00:00"
    assert result[0]["date_edited"] == "2022-03-19 00:00:00"
