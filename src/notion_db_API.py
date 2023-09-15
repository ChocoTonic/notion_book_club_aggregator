import logging
import os
from typing import Dict

from dotenv import load_dotenv
from notion_client import AsyncClient
from notion_client.errors import APIResponseError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


retry_decorator = retry(
    wait=wait_fixed(1),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(APIResponseError),
)


class NotionDBAPI:
    """
    A class for interacting with Notion databases using the Notion API.

    Args:
        token (str): The Notion API token. If not provided, it will be fetched from the environment variable NOTION_TOKEN.
        database_id (str): The ID of the Notion database to work with. If not provided, it will be fetched from the environment variable NOTION_DATABASE_ID.
    """

    def __init__(self, token=None, database_id=None):
        self.notion = AsyncClient(auth=token or os.getenv("NOTION_TOKEN"))
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")

    @retry_decorator
    async def query_database(self):
        """
        Query the Notion database.

        Returns:
            dict: The query result from the Notion database.
        """
        return await self.notion.databases.query(database_id=self.database_id)

    @retry_decorator
    async def add_page(self, properties: Dict):
        """
        Add a new page to the Notion database with the specified properties.

        Args:
            properties (dict): A dictionary of property values for the new page.

        Returns:
            dict: The created Notion page.
        """
        return await self.notion.pages.create(
            parent={"database_id": self.database_id}, properties=properties
        )

    @retry_decorator
    async def update_page(self, page_id: str, properties: Dict):
        """
        Update an existing Notion page with the specified properties.

        Args:
            page_id (str): The ID of the page to update.
            properties (dict): A dictionary of property values to update.

        Returns:
            dict: The updated Notion page.
        """
        return await self.notion.pages.update(page_id=page_id, properties=properties)

    @retry_decorator
    async def archive_page(self, page_id: str):
        """
        Archive (mark as archived) an existing Notion page.

        Args:
            page_id (str): The ID of the page to archive.

        Returns:
            dict: The archived Notion page.
        """
        return await self.notion.pages.update(page_id=page_id, archived=True)
