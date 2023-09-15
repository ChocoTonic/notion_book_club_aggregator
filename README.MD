# Notion Book Club Aggregator

This project updates a Notion database with book entries and their average ratings and favorite counts.

## Demo

![](demo/demo_notion_book_club_aggregator.gif)

## File Structure

```bash
notion_book_club_aggregator/
.env_example
README.MD
data/
    ratings.csv
pytest.ini
requirements.txt
run_tests.sh
src/
    __init__.py
    book.py
    book_club_aggregator.py
    book_manager.py
    csv_reader.py
    main.py
    member.py
    normalizer.py
    notion_db_API.py
    rating.py
    tests/
        __init__.py
        test_book.py
        test_csv_reader.py
        test_files/
            test_ratings.csv
        test_member.py
        test_normalizer.py
        test_rating.py
venv_setup_run.sh
```

## Setup and Installation

1. Make sure you have Python 3.8 or higher installed.
1. Run `./venv_setup_run.sh` to setup a virtual environment and install the required dependencies and run the program.

## Getting Started

Create a Notion integration to obtain a Notion Integration Secret Key.

Connect the integration to your Notion database by adding it as a connection in the database settings.

Retrieve the database ID from the URL of the database you want to populate. The database ID is the string of characters found after `notion.so/` in the URL.

Clone the repository or download the zip file, then extract its contents.

Save the Notion Integration Secret Key and the database ID as environment variables or in a `.env` file. To do this, copy the contents of `.env.example` to a new `.env` file and replace the placeholder values with your actual data.

Example of a `.env` file:

```bash
NOTION_TOKEN=[NOTION_INTEGRATION_SECRET_KEY]
NOTION_DATABASE_ID=[NOTION_DATABASE_ID]
```

## Usage

[Unix-based Systems (Linux, macOS, etc.)](#unix-based-systems-linux-macos-etc)

[Windows Systems](#windows-systems)

### Unix-based Systems (Linux, macOS, etc.)

The below shell script will set up a virtual environment, install the required dependencies, and execute the program.

```bash
./venv_setup_run.sh
```

To modify the data that populates the database, make necessary changes to the CSV file located at `data/ratings.csv`.

If you wish to run the program with the default CSV file, ensure you've previously executed the `./venv_setup_run.sh` script and set the environment variables.

```bash
python src/main.py
```

If you want to use a different CSV file, run the program with the following command:

```
python src/main.py --csv_path <path-to-csv-file>
```

Alternatively, it is possible to manually set up a virtual environment and install the required dependencies.

1. Navigate to the project root directory using the terminal.
1. Set up a virtual environment by running:

```bash
python -m venv myenv
source myenv/bin/activate
```

1. Install the necessary dependencies with:

```bash
pip install -r requirements.txt
```

And proceed to run the program as described above.

## Architecture

The program is structured as a Python package with a `src` directory containing the source code and a `tests` directory containing the unit tests.

The `src` directory contains the following modules:

![Class Diagram](https://mermaid.ink/svg/pako:eNqNVUuP2jAQ_iuRT614iADhkUMlFi49sKp2pR6qSNGQDMGqY6e2g5ZF_Pc6D0ocAmouSb75PP7m4fGZRCJG4pOIgVIbComENOCOeUrE2QLlzrlCLgFvml6E-L1m-W6VJBIT0EJeicUz2Bmz8p0NjfQN7WVSRKhUGKljGIOGL18bxpiqjMEpVBq0sixQ74Fh4dYmdMjaAocEbT2QUd95FZoKvnlZ_fjeMBVCdqAwpLHvKC0bJl4u8J2VOvFozSjyZjQJ6hA_qNKUJ6GE4mXrtgildONAUrRZeaZQ6tKuQi3Cqx47BXFcMlor42tS7EwiQ4MDY5XXO1GmDpnZs6GkI41W_jTVDNvpqWO-K3MhtrLZMRxRmsJ0mSKRcx3u4Sgk1Q9Vrd9_viHEdml70kBWN7VWbTHdtbqBQ_rfwch2ilvuX4VMgdHPlip-hcNis4dr_zWkre9Z3z1p2N6fHOXpcQdlJv1dHXSHg4wO9Nhh2KOODgVMuVloyowqZw9P41uZUyu0tKyGX1elNTH8svGaicjT4rhLU5Y9E6Bbu5TzaTD4duuMFt4YBx0We35VhI65VtBvVX5Ka0b1gHKLsDmrqj1a4-meYIuo02t7bYBNNfUpKOCKEXDSJykajzQ2V0BZo4DoA6YYEN98MpocdEACfjFEyLV4N81IfC1z7JOqceorg_h7YMqgGFMT5ra-VIpXn2TAfwlx45h_4p_JB_EHnjv0pu50ORvPZwvPm8775GRgdz6cLiZLd-lOJ7P5bO4tLn3yWfpwh6OR4Y2Xo_HSm03chXf5C9EyDpE)

## Challenges and Resolutions

I wanted to challenge myself by creating a Typescript project from scratch. It took longer to define types but in the end it was helpful to understand exactly the data I was transforming. Below are resources and challenges I ran into:

1. [Notion Adding Connection Help Page](https://www.notion.so/help/add-and-manage-connections-with-the-api#add-connections-to-pages): Helpful resource for adding connection to Notion database

    - Challenge: the take home instructions could have directly linked to this to save me some time looking for how to add the connection to the integration since it was not obvious where to find it.
    - Resolution: I found this resource by searching for "notion add connection" on Google

1. [Notion Python SDK](https://github.com/ramnes/notion-sdk-py): The wrappers were helpful abstractions to the Notion API

    - Challenge: The documentation was not very clear or missing from the API reference for python SDK.
    - Resolution: Looked directly at the source code to understand what the methods were doing and how to use them and then wrote my own documentation in the docstrings of my functions.

1. [python-dotenv](https://www.npmjs.com/package/dotenv): To load environment variables from a `.env` file.

    - Challenge: I was having trouble loading the environment variables from the `.env` file for test runs.
    - Resolution: Searched for "python load environment variables from .env file" on Google and found this library. It was very easy to use and I was able to load the environment variables from the `.env` file for test runs.

1. [pytest](https://docs.pytest.org/en/7.4.x/): To run unit tests

    - Challenge: Got stuck for a while trying to figure out how to run pytest from the root directory of the project.
    - Resolution: Searched for "pytest run from root directory" on Google and found that I could use `pytest.ini` to configure pytest to run from the root directory of the project.

1. [titlecase](https://github.com/ppannuto/python-titlecase): A Python library for converting strings to title case.

    - Challenge: I wanted to normalize the book titles and member names to title case as all lower case was not very presentable.
    - Resolution: I searched for "python title case library" on Google and found this library. It was very easy to use and I was able to normalize the book titles and member names to title case.

1. [tenacity](https://github.com/jd/tenacity): A general-purpose retrying library for Python.
    - Challenge: I wanted to make sure that the program was resilient to network errors and would retry the API calls if they failed.
    - Resolution: I searched for "python retry library" on Google and found this library. It was very easy to use and I was able to configure it to retry the API calls if they failed.

## Major Sources

-   [Notion API Documentation](https://developers.notion.com/docs)

# Further Improvements

## Testing

## Unit Tests

The unit tests are located in the `tests` directory. The unit tests are run with the following command:

```bash
pytest
```

I performed testing by hand by running the program and checking the database to ensure the data was populated correctly and also by running the unit tests.

Given more time, I would have liked to add more unit tests to cover more edge cases and also add integration tests to test the program end-to-end.

Mocking the Notion API calls would have been helpful to test the program end-to-end.

Integration tests from the command line would have been helpful to test the program end-to-end.

## API Reference

The representation of the relationships between the structures involving the parent, database, and pages were not very clear in the API reference. I did eventually understand that it was like a book, chapter, and page relationship but it took me a while to understand that. An image or diagram would have been helpful to understand the relationships between the structures.
