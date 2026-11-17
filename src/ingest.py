
from pathlib import Path
import pandas as pd
import sqlite3


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "data" / "retail_sales.db"


# --------------------------------------------------
# 2. DATASET CONFIGURATION
# --------------------------------------------------

# Each CSV file is mapped to its database table.
datasets = [
    ("olist_customers_dataset.csv", "customers"),
    ("olist_sellers_dataset.csv", "sellers"),
    ("olist_products_dataset.csv", "products"),
    ("product_category_name_translation.csv", "category_translation"),
    ("olist_orders_dataset.csv", "orders"),
    ("olist_order_items_dataset.csv", "order_items"),
    ("olist_order_payments_dataset.csv", "order_payments"),
    ("olist_order_reviews_dataset.csv", "order_reviews"),
    ("olist_geolocation_dataset.csv", "geolocation")
]


# Preserve postal-code prefixes as strings.
dtype_config = {
    "olist_customers_dataset.csv": {
        "customer_zip_code_prefix": "string"
    },

    "olist_sellers_dataset.csv": {
        "seller_zip_code_prefix": "string"
    },

    "olist_geolocation_dataset.csv": {
        "geolocation_zip_code_prefix": "string"
    }
}


# --------------------------------------------------
# 3. DATA INGESTION FUNCTION
# --------------------------------------------------

def ingest_dataset(connection, file_name, table_name):

    file_path = DATA_DIR / file_name

    print("\n" + "=" * 55)
    print("Importing:", file_name)
    print("Target table:", table_name)
    print("=" * 55)

    # Check whether the CSV exists.
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    # Read CSV using Pandas.
    df = pd.read_csv(
        file_path,
        dtype=dtype_config.get(file_name),
        low_memory=False
    )

    print("CSV rows:", len(df))

    # Insert records into the existing SQLite table.
    df.to_sql(
        name=table_name,
        con=connection,
        if_exists="append",
        index=False,
        chunksize=5000
    )

    print("Records inserted:", len(df))

    return len(df)


# --------------------------------------------------
# 4. MAIN INGESTION PROCESS
# --------------------------------------------------

def main():

    # Check database existence.
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "Database not found. Run python -m src.database first."
        )

    connection = sqlite3.connect(DB_PATH)

    try:

        # Enable foreign key validation.
        connection.execute("PRAGMA foreign_keys = ON")

        # Prevent accidental duplicate imports.
        cursor = connection.cursor()

        for _, table_name in datasets:

            cursor.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            )

            existing_rows = cursor.fetchone()[0]

            if existing_rows > 0:
                raise RuntimeError(
                    f"Table '{table_name}' already contains "
                    f"{existing_rows} records. "
                    "Import stopped to prevent duplicate insertion."
                )

        print("\nStarting data ingestion...")

        ingestion_report = []

        # Import datasets in dependency order.
        for file_name, table_name in datasets:

            inserted_rows = ingest_dataset(
                connection,
                file_name,
                table_name
            )

            ingestion_report.append({
                "file_name": file_name,
                "table_name": table_name,
                "inserted_rows": inserted_rows
            })

        connection.commit()

        # Verify foreign key relationships.
        violations = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if violations:
            print("\nForeign key violations:", len(violations))
            for violation in violations[:10]:
                print(violation)
        else:
            print("\nForeign key check: PASSED")

        # Display ingestion report.
        report_df = pd.DataFrame(ingestion_report)

        print("\n" + "=" * 65)
        print("DATA INGESTION REPORT")
        print("=" * 65)

        print(report_df.to_string(index=False))

        print(
            "\nTotal records imported:",
            report_df["inserted_rows"].sum()
        )

        print("\nData ingestion completed!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()