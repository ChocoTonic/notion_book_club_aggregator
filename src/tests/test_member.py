import pytest

from book import Book
from member import Member


def test_member_attributes():
    member = Member("Alice")
    assert member.name == "Alice"
    assert member.ratings == {}


def test_rate_book_valid_rating():
    member = Member("Alice")
    book = Book("The Pragmatic Programmer")
    member.rate_book(book, 5)
    assert len(member.ratings) == 1
    assert member.ratings[book.title.lower()].num_stars == 5


def test_rate_book_invalid_rating():
    member = Member("Alice")
    book = Book("The Pragmatic Programmer")
    with pytest.raises(ValueError):
        member.rate_book(book, -1)
    with pytest.raises(ValueError):
        member.rate_book(book, 6)
