import argparse
import asyncio
import logging
import os

from dotenv import load_dotenv

from book_club_aggregator import BookClubAggregator
from book_manager import BookManager
from csv_reader import CSVReader
from notion_db_API import NotionDBAPI


async def main(ratings_file: str = None):
    load_dotenv()

    print("Initializing the Book Club Aggregator...")

    if ratings_file is None:
        # Get the current file directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Navigate up one level
        parent_dir = os.path.dirname(current_dir)

        # Define the file path for CSV data
        file_path = os.path.join(os.path.join(parent_dir, "data"), "ratings.csv")
    else:
        file_path = ratings_file

    print(f"Reading data from CSV file: '{file_path}'")

    # Read data from the CSV file
    book_data = CSVReader.read_data(file_path)
    print("Data successfully loaded from the CSV file.")
    print()

    # Create a BookClubAggregator instance
    book_club_aggregator = BookClubAggregator(book_data)

    # Display statistics
    print("Calculating and displaying statistics:")
    book_club_aggregator.display_stats()
    print()

    # Aggregate book statistics
    ratings_new = book_club_aggregator.aggregate_book_stats()
    print("Book statistics aggregated successfully.")

    # Create a book manager instance to interact with the Notion database
    book_manager = BookManager(api=NotionDBAPI())
    print("Connected to the Notion database.")

    # Get existing ratings from the Notion database
    ratings_existing = await book_manager.get_existing_ratings()
    print("Retrieved existing ratings from the Notion database.")

    print("Updating the Notion database...")

    # Update the Notion database
    await book_manager.upsert_books_to_database(ratings_new, ratings_existing)

    print("Notion database updated.")

    print("All Done! 🎊")


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)

    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description="Book Club Aggregator")

    # Add an optional argument to specify the input ratings file
    parser.add_argument(
        "--ratings-file",
        help="Input ratings file (default: use hardcoded file at 'data/ratings.csv')",
        default=None,
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with the ratings file argument
    asyncio.run(main(args.ratings_file))
