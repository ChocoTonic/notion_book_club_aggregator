import asyncio
import logging
import os
from typing import Dict, List, Union

from notion_client.errors import APIResponseError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from normalizer import Normalizer
from notion_db_API import NotionDBAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


retry_decorator = retry(
    wait=wait_fixed(1),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(APIResponseError),
)


class BookManager:
    """
    Manages the business logic for book entries.
    """

    def __init__(self, api: NotionDBAPI):
        self.api = api
        self.database_id = api.database_id or os.getenv("NOTION_DATABASE_ID")
        self.notion = api.notion

    @retry_decorator
    async def get_existing_ratings(self) -> Dict[str, Dict[str, Union[int, str]]]:
        """
        Fetches existing ratings from the Notion database.

        Returns:
            Dict[str, Dict[str, Union[int, str]]]: A dictionary containing existing ratings.
        """
        try:
            response = await self.notion.databases.query(database_id=self.database_id)
            return await self.get_existing_book_entries(response["results"])
        except APIResponseError as error:
            logger.error(f"API Error ({error.code}): {error.body}")
            return {}
        except Exception as error:
            logger.exception(f"Unexpected error: {error}")
            return {}

    @retry_decorator
    async def get_existing_book_entries(
        self, data: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Extracts existing book entries from Notion database data.

        Args:
            data (List[Dict[str, str]]): List of database entries.

        Returns:
            Dict[str, str]: A dictionary containing existing book entries.
        """
        existing_book_entries = {}
        for entry in data:
            book_title = Normalizer.normalize_name(
                entry["properties"]["Book Title"]["title"][0]["text"]["content"]
            )

            existing_book_entries[book_title] = {
                "pageId": entry["id"],
                "rating": entry["properties"]["Rating"]["number"],
                "favorites": entry["properties"]["Favorites"]["number"],
            }
        return existing_book_entries

    @retry_decorator
    async def upsert_books_to_database(
        self, new_ratings: Dict[str, Dict], existing_ratings: Dict[str, Dict]
    ) -> None:
        """
        Update or add books in the database based on new ratings.

        Args:
            new_ratings (Dict[str, Dict]): Dictionary containing new ratings.
            existing_ratings (Dict[str, Dict]): Dictionary containing existing ratings.
        """
        books_to_update = []
        books_to_add = []

        for book_title, book_stats in new_ratings.items():
            if book_title in existing_ratings:
                existing_entry = existing_ratings[book_title]

                new_average_rating = book_stats["rating"]
                new_favorites = book_stats["favorites"]
                existing_average_rating = existing_entry["rating"]
                existing_favorites = existing_entry["favorites"]

                if (
                    new_average_rating != existing_average_rating
                    or new_favorites != existing_favorites
                ):
                    updated_entry = await self.get_properties(
                        {
                            **book_stats,
                            "Book Title": book_title,
                            "pageId": existing_entry["pageId"],
                        }
                    )
                    books_to_update.append(updated_entry)
            else:
                new_entry = {**book_stats, "book": book_title}
                books_to_add.append(new_entry)

        for entry in books_to_update:
            await self.update_book(entry)

        for entry in books_to_add:
            await self.add_book(entry)

    @retry_decorator
    async def add_book(self, book_entry: Dict):
        """
        Add a new book entry to the Notion database.

        Args:
            book_entry (Dict): A dictionary containing book entry data.
        """
        try:
            return await self.api.add_page(await self.get_properties(book_entry))
        except APIResponseError as error:
            logger.error(f"API Error ({error.code}): {error.body}")
        except Exception as error:
            logger.exception(f"Unexpected error: {error}")

    @retry_decorator
    async def update_book(self, updated_book_entry: Dict):
        """
        Update an existing book entry in the Notion database.

        Args:
            updated_book_entry (Dict): A dictionary containing updated book entry data.
        """
        try:
            return await self.api.update_page(
                updated_book_entry["pageId"], self.get_properties(updated_book_entry)
            )
        except APIResponseError as error:
            logger.error(f"API Error ({error.code}): {error.body}")
        except Exception as error:
            logger.exception(f"Unexpected error: {error}")

    @retry_decorator
    async def delete_all_books(self):
        """
        Delete all books from the Notion database.
        """
        try:
            entries = await self.api.query_database()
            for entry in entries["results"]:
                await self.api.archive_page(entry["id"])

        except APIResponseError as error:
            logger.error(f"API Error ({error.code}): {error.body}")
        except Exception as error:
            logger.exception(f"Unexpected error: {error}")

    async def get_properties(
        self, book_entry: Dict[str, Union[str, float]]
    ) -> Dict[str, Dict]:
        """
        Constructs the properties of a book entry for Notion.

        Args:
            book_entry (Dict[str, Union[str, float]]): A dictionary containing book entry data.

        Returns:
            Dict[str, Dict]: A dictionary containing the properties of a book entry for Notion.
        """
        return {
            "Book Title": {"title": [{"text": {"content": book_entry["book"]}}]},
            "Rating": {"number": book_entry["rating"]},
            "Favorites": {"number": book_entry["favorites"]},
        }


async def main():
    # Get the Notion API token from the environment variable
    token = os.getenv("NOTION_TOKEN")

    # Print the last 4 characters of the token (for debugging)
    print(f"Token: {token[-4:]}")

    # Initialize the Notion database
    notion_databases = BookManager(NotionDBAPI())

    # Delete all books
    await notion_databases.delete_all_books()

    # Define new ratings
    new_ratings = {
        "The Hobbit": {"rating": 5, "favorites": 1},
        "The Fellowship of the Ring": {"rating": 5, "favorites": 1},
    }

    # Get the current database entries
    existing_ratings = await notion_databases.get_existing_ratings()

    # Update the database with new ratings
    await notion_databases.upsert_books_to_database(
        new_ratings=new_ratings, existing_ratings=existing_ratings
    )

    # Delete all books
    await notion_databases.delete_all_books()


if __name__ == "__main__":
    asyncio.run(main())
