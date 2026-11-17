from pathlib import Path
import sqlite3
import pandas as pd


# --------------------------------------------------
# 1. DATABASE CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "retail_sales.db"


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    return connection


# --------------------------------------------------
# 2. TOTAL SALES ANALYSIS
# --------------------------------------------------

def get_total_sales(delivered_only=True):

    status_filter = (
        "WHERE o.order_status = 'delivered'"
        if delivered_only else ""
    )

    query = f"""
        SELECT

            ROUND(SUM(oi.price), 2)
                AS product_sales,

            ROUND(SUM(oi.freight_value), 2)
                AS freight_value,

            ROUND(SUM(oi.price + oi.freight_value), 2)
                AS total_including_freight

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        {status_filter}
    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(query, connection)

        return df.iloc[0].to_dict()

    finally:
        connection.close()


# --------------------------------------------------
# 3. MONTHLY SALES ANALYSIS
# --------------------------------------------------

def get_monthly_sales():

    query = """

        SELECT

            strftime(
                '%Y-%m',
                o.order_purchase_timestamp
            ) AS sales_month,

            ROUND(SUM(oi.price), 2)
                AS monthly_product_sales,

            COUNT(DISTINCT o.order_id)
                AS total_orders

        FROM orders o

        JOIN order_items oi
            ON o.order_id = oi.order_id

        WHERE o.order_status = 'delivered'

        GROUP BY sales_month

        ORDER BY sales_month

    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(query, connection)

        return df

    finally:
        connection.close()


# --------------------------------------------------
# 4. TOP PRODUCTS ANALYSIS
# --------------------------------------------------

def get_top_products(limit=10):

    query = """

        SELECT

            p.product_id,

            COALESCE(
                t.product_category_name_english,
                p.product_category_name,
                'unknown'
            ) AS product_category,

            COUNT(*) AS order_lines,

            ROUND(SUM(oi.price), 2)
                AS total_product_sales

        FROM order_items oi

        JOIN products p
            ON oi.product_id = p.product_id

        LEFT JOIN category_translation t
            ON p.product_category_name =
               t.product_category_name

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.order_status = 'delivered'

        GROUP BY
            p.product_id,
            product_category

        ORDER BY total_product_sales DESC

        LIMIT ?

    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(
            query,
            connection,
            params=(limit,)
        )

        return df

    finally:
        connection.close()


# --------------------------------------------------
# 5. PRODUCT CATEGORY ANALYSIS
# --------------------------------------------------

def get_category_sales(limit=10):

    query = """

        SELECT

            COALESCE(
                t.product_category_name_english,
                p.product_category_name,
                'unknown'
            ) AS category,

            COUNT(*) AS order_lines,

            ROUND(SUM(oi.price), 2)
                AS total_product_sales

        FROM order_items oi

        JOIN products p
            ON oi.product_id = p.product_id

        LEFT JOIN category_translation t
            ON p.product_category_name =
               t.product_category_name

        JOIN orders o
            ON oi.order_id = o.order_id

        WHERE o.order_status = 'delivered'

        GROUP BY category

        ORDER BY total_product_sales DESC

        LIMIT ?

    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(
            query,
            connection,
            params=(limit,)
        )

        return df

    finally:
        connection.close()


# --------------------------------------------------
# 6. STATE-WISE SALES ANALYSIS
# --------------------------------------------------

def get_state_sales():

    query = """

        SELECT

            c.customer_state,

            COUNT(DISTINCT o.order_id)
                AS total_orders,

            ROUND(SUM(oi.price), 2)
                AS total_product_sales

        FROM customers c

        JOIN orders o
            ON c.customer_id = o.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        WHERE o.order_status = 'delivered'

        GROUP BY c.customer_state

        ORDER BY total_product_sales DESC

    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(query, connection)

        return df

    finally:
        connection.close()


# --------------------------------------------------
# 7. PAYMENT ANALYSIS
# --------------------------------------------------

def get_payment_analysis():

    query = """

        SELECT

            payment_type,

            COUNT(*) AS payment_records,

            COUNT(DISTINCT order_id)
                AS unique_orders,

            ROUND(SUM(payment_value), 2)
                AS total_payment_value

        FROM order_payments

        GROUP BY payment_type

        ORDER BY total_payment_value DESC

    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(query, connection)

        return df

    finally:
        connection.close()


# --------------------------------------------------
# 8. DELIVERY PERFORMANCE ANALYSIS
# --------------------------------------------------

def get_delivery_performance():

    query = """

        SELECT

            COUNT(*) AS delivered_orders,

            ROUND(
                AVG(
                    julianday(order_delivered_customer_date) -
                    julianday(order_purchase_timestamp)
                ),
                2
            ) AS average_delivery_days,

            ROUND(
                AVG(
                    julianday(order_delivered_customer_date) -
                    julianday(order_estimated_delivery_date)
                ),
                2
            ) AS average_days_vs_estimate

        FROM orders

        WHERE order_status = 'delivered'

        AND order_delivered_customer_date IS NOT NULL

        AND order_purchase_timestamp IS NOT NULL

        AND order_estimated_delivery_date IS NOT NULL

    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(query, connection)

        return df.iloc[0].to_dict()

    finally:
        connection.close()


# --------------------------------------------------
# 9. ORDER STATUS ANALYSIS
# --------------------------------------------------

def get_order_status():

    query = """

        SELECT

            order_status,

            COUNT(*) AS total_orders

        FROM orders

        GROUP BY order_status

        ORDER BY total_orders DESC

    """

    connection = get_connection()

    try:

        df = pd.read_sql_query(query, connection)

        return df

    finally:
        connection.close()


# --------------------------------------------------
# 10. RUN ANALYTICS FUNCTIONS
# --------------------------------------------------

if __name__ == "__main__":

    print("\n========== PYTHON ANALYTICS RESULTS ==========")

    print("\n--- TOTAL SALES ---")
    print(get_total_sales())

    print("\n--- MONTHLY SALES ---")
    print(get_monthly_sales().to_string(index=False))

    print("\n--- TOP 10 PRODUCTS ---")
    print(get_top_products().to_string(index=False))

    print("\n--- TOP 10 CATEGORIES ---")
    print(get_category_sales().to_string(index=False))

    print("\n--- STATE-WISE SALES ---")
    print(get_state_sales().to_string(index=False))

    print("\n--- PAYMENT ANALYSIS ---")
    print(get_payment_analysis().to_string(index=False))

    print("\n--- DELIVERY PERFORMANCE ---")
    print(get_delivery_performance())

    print("\n--- ORDER STATUS ---")
    print(get_order_status().to_string(index=False))

    print("\nPython analytics completed successfully!")

