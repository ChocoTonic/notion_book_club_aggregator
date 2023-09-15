import pytest

from book import Book
from member import Member
from rating import Rating


def test_rating_attributes():
    member = Member("Alice")
    book = Book("The Pragmatic Programmer")
    rating = Rating(member, book, 5)
    assert rating.member == member
    assert rating.book == book
    assert rating.num_stars == 5


def test_rating_invalid_num_stars():
    member = Member("Alice")
    book = Book("The Pragmatic Programmer")
    with pytest.raises(ValueError):
        _ = Rating(member, book, -1)
    with pytest.raises(ValueError):
        _ = Rating(member, book, 6)
