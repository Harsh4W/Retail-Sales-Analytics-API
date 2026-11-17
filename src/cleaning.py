
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "Raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. DATASET CONFIGURATION
# --------------------------------------------------

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

# Date columns that need conversion
date_columns = {
    "olist_orders_dataset.csv": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ],

    "olist_order_items_dataset.csv": [
        "shipping_limit_date"
    ],

    "olist_order_reviews_dataset.csv": [
        "review_creation_date",
        "review_answer_timestamp"
    ]
}

# Postal codes are identifiers, not numerical measurements.
# Read them as strings to preserve leading zeros.
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
# 3. DATA CLEANING FUNCTION
# --------------------------------------------------

def clean_dataset(file_name):

    file_path = RAW_DIR / file_name

    print("\n" + "=" * 60)
    print("Cleaning:", file_name)
    print("=" * 60)

    # Load original CSV
    df = pd.read_csv(
        file_path,
        dtype=dtype_config.get(file_name),
        low_memory=False
    )

    original_rows = len(df)

    # Check missing values before cleaning
    missing_before = int(df.isnull().sum().sum())

    print("Original rows:", original_rows)
    print("Missing values before cleaning:", missing_before)

    # ----------------------------------------------
    # 3A. REMOVE EXACT DUPLICATE ROWS
    # ----------------------------------------------

    duplicate_count = int(df.duplicated().sum())

    df = df.drop_duplicates()

    print("Exact duplicate rows removed:", duplicate_count)

    # ----------------------------------------------
    # 3B. CONVERT DATE COLUMNS
    # ----------------------------------------------

    for column in date_columns.get(file_name, []):

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    # ----------------------------------------------
    # 3C. HANDLE PRODUCT CATEGORY MISSING VALUES
    # ----------------------------------------------

    if file_name == "olist_products_dataset.csv":

        df["product_category_name"] = (
            df["product_category_name"].fillna("unknown")
        )

    # ----------------------------------------------
    # 3D. VALIDATE IMPORTANT NUMERICAL VALUES
    # ----------------------------------------------

    if file_name == "olist_order_items_dataset.csv":

        print(
            "Zero or negative prices:",
            (df["price"] <= 0).sum()
        )

        print(
            "Negative freight values:",
            (df["freight_value"] < 0).sum()
        )

    if file_name == "olist_order_payments_dataset.csv":

        print(
            "Zero payment values:",
            (df["payment_value"] == 0).sum()
        )

        print(
            "Zero payment installments:",
            (df["payment_installments"] == 0).sum()
        )

    if file_name == "olist_order_reviews_dataset.csv":

        print(
            "Review scores outside 1-5:",
            (~df["review_score"].between(1, 5)).sum()
        )

    # ----------------------------------------------
    # 3E. CHECK MISSING VALUES AFTER CLEANING
    # ----------------------------------------------

    missing_after = int(df.isnull().sum().sum())

    print("Missing values after cleaning:", missing_after)
    print("Final rows:", len(df))

    # ----------------------------------------------
    # 3F. SAVE CLEANED DATASET
    # ----------------------------------------------

    output_path = PROCESSED_DIR / file_name

    df.to_csv(output_path, index=False)

    print("Saved to:", output_path)

    # Return cleaning summary
    return {
        "file_name": file_name,
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicates_removed": duplicate_count,
        "missing_before": missing_before,
        "missing_after": missing_after
    }


# --------------------------------------------------
# 4. PROCESS ALL DATASETS
# --------------------------------------------------

def main():

    cleaning_report = []

    for file_name in files:

        file_path = RAW_DIR / file_name

        if not file_path.exists():

            print("\nFILE NOT FOUND:", file_name)
            continue

        result = clean_dataset(file_name)

        cleaning_report.append(result)

    # ----------------------------------------------
    # 5. SAVE CLEANING REPORT
    # ----------------------------------------------

    if cleaning_report:

        report_df = pd.DataFrame(cleaning_report)

        report_path = REPORT_DIR / "cleaning_report.csv"

        report_df.to_csv(report_path, index=False)

        print("\n" + "=" * 60)
        print("FINAL CLEANING REPORT")
        print("=" * 60)

        print(report_df.to_string(index=False))

        print("\nCleaning process completed!")
        print("Report saved to:", report_path)


if __name__ == "__main__":
    main()
