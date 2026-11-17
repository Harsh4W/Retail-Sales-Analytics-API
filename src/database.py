
from pathlib import Path
import sqlite3

# 1. Find the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Database location
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "retail_sales.db"

# 3. SQL schema location
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    # Enable foreign key checking
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_database():

    # Ensure database folder exists
    DB_DIR.mkdir(parents=True, exist_ok=True)

    # Read SQL schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    # Create database tables
    connection = get_connection()

    try:
        connection.executescript(schema)
        connection.commit()

        print("Database created successfully!")
        print("Database location:", DB_PATH)

    finally:
        connection.close()


def verify_tables():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        tables = cursor.fetchall()

        print("\n--- DATABASE TABLES ---")

        for table in tables:
            print(table[0])

        print("\nTotal tables:", len(tables))

    finally:
        connection.close()


if __name__ == "__main__":

    create_database()
    verify_tables()
