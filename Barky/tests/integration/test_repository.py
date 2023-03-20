import pytest
from barkylib.adapters.orm import SqlAlchemyRepository
from barkylib.domain.models import Bookmark

@pytest.fixture
def sql_repo():
    return SqlAlchemyRepository()

def test_add_one(sql_repo):
    bookmark = Bookmark(title="test bookmark", url="http://example.com")
    sql_repo.add_one(bookmark)
    assert bookmark in sql_repo.seen

def test_add_many(sql_repo):
    bookmarks = [
        Bookmark(title="bookmark 1", url="http://example.com/1"),
        Bookmark(title="bookmark 2", url="http://example.com/2"),
        Bookmark(title="bookmark 3", url="http://example.com/3"),
    ]
    sql_repo.add_many(bookmarks)
    assert all(bookmark in sql_repo.seen for bookmark in bookmarks)
    
def test_get(sql_repo):
    bookmark = Bookmark(title="test bookmark", url="http://example.com")
    sql_repo.add_one(bookmark)
    assert sql_repo.get("test bookmark") == bookmark
    
def test_get_missing(sql_repo):
    assert sql_repo.get("nonexistent") is None
    
def test_edit(sql_repo):
    bookmark = Bookmark(title="test bookmark", url="http://example.com")
    sql_repo.add_one(bookmark)
    bookmark.url = "http://new.example.com"
    sql_repo.edit(bookmark)
    assert sql_repo.get("test bookmark").url == "http://new.example.com"

