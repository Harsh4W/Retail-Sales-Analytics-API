
from src.database import get_connection

connection = get_connection()

cursor = connection.cursor()

tables = [
    "customers",
    "orders",
    "order_items",
    "order_payments",
    "order_reviews",
    "products",
    "sellers",
    "geolocation",
    "category_translation"
]

for table in tables:

    print("\n" + "=" * 50)
    print("TABLE:", table)
    print("=" * 50)

    cursor.execute(f"PRAGMA table_info({table})")

    columns = cursor.fetchall()

    for column in columns:
        print(
            "Column:", column[1],
            "| Type:", column[2],
            "| Primary Key:", column[5]
        )

connection.close()

print("\nDatabase structure verified!")
