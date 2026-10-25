

import duckdb
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# Connect to DuckDB
con = duckdb.connect()

# Locate the orders CSV file
orders_path = (DATA_DIR / "olist_orders_dataset.csv").as_posix()

# Calculate total number of orders using SQL
result = con.execute(f"""
    SELECT COUNT(DISTINCT order_id) AS total_orders
    FROM read_csv_auto('{orders_path}')
""").fetchdf()

print(result)


# Locate the payments CSV file
payments_path = (DATA_DIR / "olist_order_payments_dataset.csv").as_posix()

# Calculate total payment value using SQL
payment_result = con.execute(f"""
    SELECT SUM(payment_value) AS total_payment_value
    FROM read_csv_auto('{payments_path}')
""").fetchdf()

print(payment_result)


# Monthly sales analysis using SQL
monthly_sales = con.execute(f"""
    SELECT
        DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS sales_month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(p.payment_value), 2) AS total_payment
    FROM read_csv_auto('{orders_path}') AS o
    JOIN read_csv_auto('{payments_path}') AS p
        ON o.order_id = p.order_id
    GROUP BY sales_month
    ORDER BY sales_month
""").fetchdf()

print(monthly_sales)


# Locate the order items and products CSV files
items_path = (DATA_DIR / "olist_order_items_dataset.csv").as_posix()
products_path = (DATA_DIR / "olist_products_dataset.csv").as_posix()

# Product category analysis
category_sales = con.execute(f"""
    SELECT
        COALESCE(p.product_category_name, 'Unknown') AS product_category,
        COUNT(oi.order_item_id) AS total_items,
        ROUND(SUM(oi.price), 2) AS total_sales,
        ROUND(AVG(oi.price), 2) AS average_item_price
    FROM read_csv_auto('{items_path}') AS oi
    JOIN read_csv_auto('{products_path}') AS p
        ON oi.product_id = p.product_id
    GROUP BY product_category
    ORDER BY total_sales DESC
    LIMIT 10
""").fetchdf()

print(category_sales)


# Delivery performance analysis using SQL
delivery_result = con.execute(f"""
    WITH delivery_data AS (
        SELECT
            order_id,
            CAST(order_purchase_timestamp AS TIMESTAMP) AS purchase_date,
            CAST(order_delivered_customer_date AS TIMESTAMP) AS delivery_date,
            CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_date
        FROM read_csv_auto('{orders_path}')
        WHERE order_status = 'delivered'
    ),
    valid_delivery AS (
        SELECT
            order_id,
            DATE_DIFF('second', purchase_date, delivery_date)
                / 86400.0 AS delivery_days,
            DATE_DIFF(
                'day',
                CAST(estimated_date AS DATE),
                CAST(delivery_date AS DATE)
            ) AS delay_days
        FROM delivery_data
        WHERE delivery_date IS NOT NULL
          AND purchase_date IS NOT NULL
          AND estimated_date IS NOT NULL
    )
    SELECT
        COUNT(*) AS total_valid_orders,
        ROUND(AVG(delivery_days), 2) AS average_delivery_days,
        SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END) AS late_orders,
        SUM(CASE WHEN delay_days <= 0 THEN 1 ELSE 0 END)
            AS on_time_or_early_orders,
        ROUND(
            100.0 * SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END)
            / COUNT(*),
            2
        ) AS late_delivery_rate_pct
    FROM valid_delivery
""").fetchdf()

print(delivery_result.to_string(index=False))
