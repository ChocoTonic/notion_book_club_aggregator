from typing import Dict


class Member:
    """
    Represents a member of a book club who rates books.
    """

    def __init__(self, name: str):
        self.name = name
        self.ratings: Dict[str, "Rating"] = {}

    def rate_book(self, book: "Book", num_stars: int):
        """
        Rates a book and associates the rating with the member.

        Args:
            book (Book): The book to be rated.
            num_stars (int): The number of stars given to the book.
        """
        from rating import Rating

        rating = Rating(self, book, num_stars)
        self.ratings[book.title] = rating
        book.add_rating(self, rating)
