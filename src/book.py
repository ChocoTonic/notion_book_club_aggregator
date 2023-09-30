from typing import Dict

from rating import Rating


class Book:
    """
    Represents a book and its associated ratings from members of a book club.
    """

    def __init__(self, title: str):
        self.title = title.lower().strip()
        self.ratings: Dict[str, Rating] = {}

    def add_rating(self, member: str, rating: Rating):
        """
        Adds a rating by a member to the book.

        Args:
            member (str): The name of the member providing the rating.
            rating (Rating): The rating given by the member.
        """
        self.ratings[member] = rating

    def average_rating(self) -> float:
        """
        Calculates and returns the average rating of the book.

        Returns:
            float: The average rating of the book.
        """
        return sum(rating.num_stars for rating in self.ratings.values()) / len(
            self.ratings
        )

    def count_favorites(self) -> int:
        """
        Counts and returns the number of ratings that are favorites (score of 5).

        Returns:
            int: The number of favorite ratings for the book.
        """
        return sum(1 for rating in self.ratings.values() if rating.num_stars == 5)

    def count_least_favorites(self) -> int:
        """
        Counts and returns the number of ratings that are favorites (score of 0).

        Returns:
            int: The number of favorite ratings for the book.
        """
        return sum(1 for rating in self.ratings.values() if rating.num_stars == 0)

    def __repr__(self):
        return f"Book({self.title})"

    def __str__(self):
        return self.title


if __name__ == "__main__":
    pass
