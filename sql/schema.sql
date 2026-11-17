
-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- 1. CUSTOMERS
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT NOT NULL,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT
);

-- 2. SELLERS
CREATE TABLE IF NOT EXISTS sellers (
    seller_id TEXT PRIMARY KEY,
    seller_zip_code_prefix TEXT,
    seller_city TEXT,
    seller_state TEXT
);

-- 3. PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_category_name TEXT,
    product_name_lenght REAL,
    product_description_lenght REAL,
    product_photos_qty REAL,
    product_weight_g REAL,
    product_length_cm REAL,
    product_height_cm REAL,
    product_width_cm REAL
);

-- 4. CATEGORY TRANSLATION
CREATE TABLE IF NOT EXISTS category_translation (
    product_category_name TEXT PRIMARY KEY,
    product_category_name_english TEXT
);

-- 5. ORDERS
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_status TEXT,
    order_purchase_timestamp TEXT,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

-- 6. ORDER ITEMS
CREATE TABLE IF NOT EXISTS order_items (
    order_id TEXT NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    shipping_limit_date TEXT,
    price REAL,
    freight_value REAL,

    PRIMARY KEY (order_id, order_item_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)
);

-- 7. ORDER PAYMENTS
CREATE TABLE IF NOT EXISTS order_payments (
    order_id TEXT NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value REAL,

    PRIMARY KEY (order_id, payment_sequential),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

-- 8. ORDER REVIEWS
-- review_id is not unique in the source data.
-- Use an internal ID as the primary key.
CREATE TABLE IF NOT EXISTS order_reviews (
    review_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id TEXT,
    order_id TEXT NOT NULL,
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TEXT,
    review_answer_timestamp TEXT,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

-- 9. GEOLOCATION
-- Postal-code prefixes can have multiple coordinates.
CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    geolocation_zip_code_prefix TEXT,
    geolocation_lat REAL,
    geolocation_lng REAL,
    geolocation_city TEXT,
    geolocation_state TEXT
);

-- INDEXES FOR COMMON JOIN COLUMNS

CREATE INDEX IF NOT EXISTS idx_orders_customer
ON orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product
ON order_items(product_id);

CREATE INDEX IF NOT EXISTS idx_order_items_seller
ON order_items(seller_id);

CREATE INDEX IF NOT EXISTS idx_order_payments_order
ON order_payments(order_id);

CREATE INDEX IF NOT EXISTS idx_order_reviews_order
ON order_reviews(order_id);

CREATE INDEX IF NOT EXISTS idx_products_category
ON products(product_category_name);

CREATE INDEX IF NOT EXISTS idx_customers_zip
ON customers(customer_zip_code_prefix);

CREATE INDEX IF NOT EXISTS idx_sellers_zip
ON sellers(seller_zip_code_prefix);

CREATE INDEX IF NOT EXISTS idx_geolocation_zip
ON geolocation(geolocation_zip_code_prefix);




