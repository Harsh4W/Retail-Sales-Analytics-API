
from pathlib import Path
import sqlite3
import pandas as pd

# 1. Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "retail_sales.db"
SQL_PATH = BASE_DIR / "sql" / "analytics.sql"


# 2. Read SQL file
with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_content = file.read()


# 3. Split SQL statements
queries = [
    query.strip()
    for query in sql_content.split(";")
    if query.strip()
]


# 4. Connect to SQLite
connection = sqlite3.connect(DB_PATH)

try:

    print("\n========== SQL ANALYTICS RESULTS ==========")

    # 5. Execute each query
    for index, query in enumerate(queries, start=1):

        print("\n" + "=" * 60)
        print(f"QUERY {index}")
        print("=" * 60)

        result = pd.read_sql_query(
            query,
            connection
        )

        print(result.to_string(index=False))

    print("\nAll SQL queries executed successfully!")

finally:
    connection.close()
