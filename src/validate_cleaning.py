
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Check date conversion
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")

print("\n--- ORDER DATE TYPES ---")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column], errors="coerce"
    )
    print(column, ":", orders[column].dtype)

# Check postal code types
customers = pd.read_csv(
    DATA_DIR / "olist_customers_dataset.csv",
    dtype={
        "customer_zip_code_prefix": "string"
    }
)

print("\n--- CUSTOMER POSTAL CODE TYPE ---")
print(customers["customer_zip_code_prefix"].dtype)

# Check product categories
products = pd.read_csv(
    DATA_DIR / "olist_products_dataset.csv"
)

print("\n--- PRODUCT CATEGORY CHECK ---")
print(products["product_category_name"].isnull().sum())
print(
    products["product_category_name"]
    .value_counts()
    .head()
)

# Check geolocation duplicates
geo = pd.read_csv(
    DATA_DIR / "olist_geolocation_dataset.csv"
)

print("\n--- GEOLOCATION CHECK ---")
print("Rows:", len(geo))
print("Exact duplicates:", geo.duplicated().sum())

print("\nValidation completed!")


