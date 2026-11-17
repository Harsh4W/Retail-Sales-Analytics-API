
from pathlib import Path
import pandas as pd
import gc

# 1. Find the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Find the raw data folder
DATA_DIR = BASE_DIR / "data" / "raw"

# 3. List the expected dataset files
files = [
    "olist_customers_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv"
]

# 4. Columns that may act as identifiers
identifier_columns = {
    "olist_customers_dataset.csv": ["customer_id", "customer_unique_id"],
    "olist_orders_dataset.csv": ["order_id", "customer_id"],
    "olist_order_items_dataset.csv": ["order_id", "product_id", "seller_id"],
    "olist_order_payments_dataset.csv": ["order_id"],
    "olist_order_reviews_dataset.csv": ["review_id", "order_id"],
    "olist_products_dataset.csv": ["product_id"],
    "olist_sellers_dataset.csv": ["seller_id"],
    "olist_geolocation_dataset.csv": ["geolocation_zip_code_prefix"],
    "product_category_name_translation.csv": ["product_category_name"]
}

print("\n========== OLIST DATASET INSPECTION ==========")

# 5. Check whether all files exist
missing_files = []

for file_name in files:
    file_path = DATA_DIR / file_name

    if file_path.exists():
        size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"FOUND: {file_name} ({size_mb:.2f} MB)")
    else:
        print(f"MISSING: {file_name}")
        missing_files.append(file_name)

if missing_files:
    print("\nPlease add the missing CSV files before continuing.")
else:
    print("\nAll nine CSV files are present.")

# 6. Inspect each CSV file
if not missing_files:
    for file_name in files:
        file_path = DATA_DIR / file_name

        print("\n" + "=" * 65)
        print(f"FILE: {file_name}")
        print("=" * 65)

        # Read CSV
        df = pd.read_csv(file_path, low_memory=False)

        # Display first three records
        print("\n--- FIRST THREE RECORDS ---")
        print(df.head(3).to_string(index=False))

        # Display dimensions
        print("\n--- DATASET SHAPE ---")
        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])

        # Display column names
        print("\n--- COLUMN NAMES ---")
        print(df.columns.tolist())

        # Display data types and non-null counts
        print("\n--- DATASET INFORMATION ---")
        df.info()

        # Display missing values
        print("\n--- MISSING VALUES ---")
        missing = df.isnull().sum()
        print(missing[missing > 0] if missing.any() else "No missing values")

        # Display duplicate records
        print("\n--- DUPLICATE RECORDS ---")
        print(df.duplicated().sum())

        # Display numerical summary
        print("\n--- NUMERICAL SUMMARY ---")
        print(df.describe().to_string())

        # Inspect identifier columns
        print("\n--- IDENTIFIER COLUMN ANALYSIS ---")
        for column in identifier_columns[file_name]:
            if column in df.columns:
                print(
                    f"{column}: "
                    f"{df[column].nunique(dropna=True)} unique values"
                )

        # Release memory before reading the next file
        del df
        gc.collect()

    print("\n========== INSPECTION COMPLETED ==========")
