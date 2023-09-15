import os

import pytest

from csv_reader import CSVReader


def test_read_data():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test_files",
        "test_ratings.csv",
    )
    expected_data = [
        {
            "book_title": "The Pragmatic Programmer",
            "member_name": "Alice",
            "num_stars": "5",
        },
        {"book_title": "Clean Code", "member_name": "Bob", "num_stars": "4"},
        {"book_title": "Code Complete", "member_name": "Charlie", "num_stars": "3"},
    ]
    assert CSVReader.read_data(file_path) == expected_data


def test_read_data_file_not_found():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test_files",
        "test_ratings_not_found.csv",
    )
    with pytest.raises(FileNotFoundError):
        CSVReader.read_data(file_path)
