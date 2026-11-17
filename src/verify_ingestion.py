
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "retail_sales.db"

connection = sqlite3.connect(DB_PATH)

# Expected record counts from cleaned datasets
expected_counts = {
    "customers": 99441,
    "sellers": 3095,
    "products": 32951,
    "category_translation": 71,
    "orders": 99441,
    "order_items": 112650,
    "order_payments": 103886,
    "order_reviews": 99224,
    "geolocation": 738332
}

results = []

print("\n--- DATABASE ROW COUNT VERIFICATION ---")

for table, expected in expected_counts.items():

    query = f"SELECT COUNT(*) FROM {table}"

    actual = pd.read_sql_query(
        query,
        connection
    ).iloc[0, 0]

    status = "PASSED" if actual == expected else "MISMATCH"

    print(
        f"{table}: Expected = {expected}, "
        f"Actual = {actual}, Status = {status}"
    )

    results.append({
        "table": table,
        "expected_rows": expected,
        "actual_rows": actual,
        "status": status
    })

# Check foreign key integrity
violations = connection.execute(
    "PRAGMA foreign_key_check"
).fetchall()

print("\n--- FOREIGN KEY VALIDATION ---")

if len(violations) == 0:
    print("No foreign key violations found.")
else:
    print("Foreign key violations:", len(violations))
    print(violations[:10])

connection.close()

# Display final report
report = pd.DataFrame(results)

print("\n--- FINAL VERIFICATION REPORT ---")
print(report.to_string(index=False))

if (report["status"] == "PASSED").all() and not violations:
    print("\nALL DATABASE CHECKS PASSED!")
else:
    print("\nSOME DATABASE CHECKS FAILED. INVESTIGATION REQUIRED.")
