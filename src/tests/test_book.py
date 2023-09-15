from book import Book
from rating import Rating


def test_add_rating():
    book = Book("The Great Gatsby")
    member_name = "Alice"
    rating = Rating(book=book, member=member_name, num_stars=4)
    book.add_rating(member_name, rating)
    assert book.ratings == {"Alice": rating}


def test_average_rating():
    book = Book("The Great Gatsby")
    book.add_rating("Alice", Rating(book, "Alice", 4))
    book.add_rating("Bob", Rating(book, "Bob", 3))
    book.add_rating("Charlie", Rating(book, "Charlie", 5))
    assert book.average_rating() == 4.0


def test_count_favorites():
    book = Book("The Great Gatsby")
    book.add_rating("Alice", Rating(book, "Alice", 4))
    book.add_rating("Bob", Rating(book, "Bob", 5))
    book.add_rating("Charlie", Rating(book, "Charlie", 5))
    assert book.count_favorites() == 2
