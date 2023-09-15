import csv
import os
from pprint import pprint
from typing import Dict, List


class CSVReader:
    """
    A utility class for reading data from CSV files.
    """

    @staticmethod
    def read_data(file_path: str) -> List[Dict[str, str or float]]:
        """
        Reads data from a CSV file and returns it as a list of dictionaries.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            List[Dict[str, str or float]]: A list of dictionaries where each dictionary represents a row from the CSV.
                The keys for each dictionary are 'book_title', 'member_name', and 'num_stars'.
        """
        try:
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                data = []
                for row in reader:
                    data.append(
                        {
                            "book_title": row[0],
                            "member_name": row[1],
                            "num_stars": row[2],
                        }
                    )
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as error:
            raise Exception(f"Unexpected error: {error}")


if __name__ == "__main__":
    file_path_ratings = os.path.join(
        os.path.dirname(os.getcwd()), "data", "ratings.csv"
    )

    ratings = CSVReader.read_data(file_path=file_path_ratings)
    pprint(ratings)
