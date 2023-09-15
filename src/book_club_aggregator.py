import logging
from typing import Dict, List, Union

from book import Book
from member import Member
from normalizer import Normalizer

logging.basicConfig(level=logging.ERROR)


class BookClubAggregator:
    """
    A class for aggregating and displaying statistics for a book club's reading data.
    """

    def __init__(self, csv_data: List[Dict[str, Union[str, float]]]):
        """
        Initialize a BookClubAggregator object.

        Args:
            csv_data (List[Dict[str, Union[str, float]]]): A list of dictionaries containing book ratings data.
        """
        self.books: Dict[str, Book] = self.process_csv_data(csv_data)

    def process_csv_data(
        self, csv_data: List[Dict[str, Union[str, float]]]
    ) -> Dict[str, Book]:
        """
        Process CSV data and return a dictionary of books.

        Args:
            csv_data (List[Dict[str, Union[str, float]]]): A list of dictionaries containing book ratings data.

        Returns:
            Dict[str, Book]: A dictionary mapping book names to Book objects.
        """
        book_data: Dict[str, Book] = {}
        member_data: Dict[str, Member] = {}

        for row in csv_data:
            book_title = Normalizer.normalize_name(row["book_title"])
            member_name = Normalizer.normalize_name(row["member_name"])
            rating = float(row["num_stars"])

            if book_title not in book_data:
                book_data[book_title] = Book(book_title)

            if member_name not in member_data:
                member_data[member_name] = Member(member_name)

            member_data[member_name].rate_book(
                book=book_data[book_title], num_stars=rating
            )

        return book_data

    def display_stats(self) -> None:
        """
        Display book statistics.
        """
        book_stats = self.aggregate_book_stats()

        max_title_length = max(len(title) for title in book_stats.keys())
        max_line_length = 120  # Total line width

        for book_title, book_stats in book_stats.items():
            avg_rating = book_stats["rating"]
            num_favorites = book_stats["favorites"]

            # Calculate the available width for the book title
            title_width = min(
                max_title_length, max_line_length - 25
            )  # Adjusted to leave space for rating and favorites

            # Print with dynamically calculated width
            print(
                f"{book_title[:title_width]:{title_width}}:\t{avg_rating} stars,\t{num_favorites} favorites"
            )

    def aggregate_book_stats(self) -> Dict[str, Dict[str, Union[float, int]]]:
        """
        Aggregate statistics for books.

        Returns:
            Dict[str, Dict[str, Union[float, int]]]: A dictionary mapping book names to dictionaries containing book statistics.
        """
        book_stats = {}
        for book_name, book in self.books.items():
            avg_rating = round(book.average_rating(), 1)
            num_favorites = book.count_favorites()
            book_stats[book_name] = {"rating": avg_rating, "favorites": num_favorites}
        return book_stats
