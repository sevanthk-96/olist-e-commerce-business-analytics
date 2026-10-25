
import pandas as pd
from pathlib import Path

# Define the folder containing the CSV files
DATA_DIR = Path(__file__).parent / "data"

# Load the Olist datasets
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
payments = pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")
customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")
sellers = pd.read_csv(DATA_DIR / "olist_sellers_dataset.csv")
reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")

# Display the number of rows and columns in each dataset
datasets = {
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Customers": customers,
    "Products": products,
    "Sellers": sellers,
    "Reviews": reviews,
}

for name, df in datasets.items():
    print(f"{name}: {df.shape[0]:,} rows, {df.shape[1]} columns")

# Preview the orders dataset
print("\nFirst five orders:")
print(orders.head())


print("\n========== DATA QUALITY REPORT ==========")

for name, df in datasets.items():
    print(f"\n--- {name} ---")

    # Column names and data types
    print("\nData types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.any() else "No missing values")

    # Duplicate rows
    print("\nDuplicate rows:", df.duplicated().sum())


print("\nOrder status counts:")
print(orders["order_status"].value_counts(dropna=False))

print("\nMissing delivery timestamps:")
print(
    orders[
        [
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ].isnull().sum()
)


print("\n========== MISSING DELIVERY DATE ANALYSIS ==========")

print("\nOrder status when carrier delivery date is missing:")
print(
    orders.loc[
        orders["order_delivered_carrier_date"].isnull(),
        "order_status"
    ].value_counts(dropna=False)
)

print("\nOrder status when customer delivery date is missing:")
print(
    orders.loc[
        orders["order_delivered_customer_date"].isnull(),
        "order_status"
    ].value_counts(dropna=False)
)


print("\n========== DELIVERED ORDERS WITH MISSING DATES ==========")

missing_dates = orders[
    (orders["order_status"] == "delivered")
    & (
        orders["order_delivered_customer_date"].isnull()
        | orders["order_delivered_carrier_date"].isnull()
    )
]

print(
    missing_dates[
        [
            "order_id",
            "order_status",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ]
)

print("\nNumber of affected orders:", len(missing_dates))


print("\n========== MISSING DATE DETAILS ==========")

print(
    missing_dates[
        [
            "order_id",
            "order_status",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ].to_string(index=False)
)

print("\nMissing carrier dates among these orders:")
print(missing_dates["order_delivered_carrier_date"].isnull().sum())

print("\nMissing customer delivery dates among these orders:")
print(missing_dates["order_delivered_customer_date"].isnull().sum())


print("\n========== BUSINESS KPIs ==========")

# Total number of orders
total_orders = orders["order_id"].nunique()
print(f"Total orders: {total_orders:,}")

# Total recorded payment value
total_payment = payments["payment_value"].sum()
print(f"Total payment value: R$ {total_payment:,.2f}")

# Average payment value per order
order_payment = payments.groupby("order_id")["payment_value"].sum()
average_order_value = order_payment.mean()
print(f"Average order value: R$ {average_order_value:,.2f}")

# Number of unique customers
unique_customers = customers["customer_unique_id"].nunique()
print(f"Unique customers: {unique_customers:,}")


print("\n========== CUSTOMER RETENTION ANALYSIS ==========")

# Connect each order to the customer's unique ID
orders_customers = orders.merge(
    customers[["customer_id", "customer_unique_id"]],
    on="customer_id",
    how="left"
)

# Count distinct orders placed by each customer
customer_order_counts = (
    orders_customers
    .dropna(subset=["customer_unique_id"])
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

# Calculate one-time and repeat customers
one_time_customers = (customer_order_counts == 1).sum()
repeat_customers = (customer_order_counts >= 2).sum()
total_customers = len(customer_order_counts)

# Calculate repeat customer rate
repeat_customer_rate = (
    repeat_customers / total_customers * 100
    if total_customers > 0 else 0
)

print(f"One-time customers: {one_time_customers:,}")
print(f"Repeat customers: {repeat_customers:,}")
print(f"Total customers with orders: {total_customers:,}")
print(f"Repeat customer rate: {repeat_customer_rate:.2f}%")


print("\n========== MONTHLY SALES ANALYSIS ==========")

# Ensure purchase timestamps are in datetime format
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

# Join orders with payment records
sales_data = orders[
    ["order_id", "order_purchase_timestamp"]
].merge(
    payments[["order_id", "payment_value"]],
    on="order_id",
    how="left"
)

# Create a month column
sales_data["month"] = (
    sales_data["order_purchase_timestamp"]
    .dt.to_period("M")
)

# Calculate monthly order count and payment value
monthly_sales = (
    sales_data.groupby("month")
    .agg(
        total_orders=("order_id", "nunique"),
        total_payment=("payment_value", "sum")
    )
    .reset_index()
)

print(monthly_sales.to_string(index=False))


print("\nEarliest purchase:")
print(orders["order_purchase_timestamp"].min())

print("\nLatest purchase:")
print(orders["order_purchase_timestamp"].max())


import matplotlib.pyplot as plt

# Convert monthly periods to strings for plotting
monthly_sales["month"] = monthly_sales["month"].astype(str)

plt.figure(figsize=(12, 5))
plt.plot(
    monthly_sales["month"],
    monthly_sales["total_payment"],
    marker="o"
)

plt.title("Monthly Payment Value - Olist E-Commerce")
plt.xlabel("Month")
plt.ylabel("Total Payment Value (R$)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


print("\n========== PRODUCT CATEGORY ANALYSIS ==========")

# Join order items with product information
items_products = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Replace missing category labels for reporting
items_products["product_category_name"] = (
    items_products["product_category_name"]
    .fillna("Unknown")
)

# Calculate sales value and item volume by category
category_performance = (
    items_products.groupby("product_category_name")
    .agg(
        total_items=("order_item_id", "count"),
        total_sales=("price", "sum"),
        average_item_price=("price", "mean")
    )
    .reset_index()
)

# Sort categories from highest to lowest sales value
category_performance = category_performance.sort_values(
    "total_sales",
    ascending=False
)

print(category_performance.head(10).to_string(index=False))


print("\n========== DELIVERY PERFORMANCE ANALYSIS ==========")

# Keep only orders marked as delivered
delivery_data = orders.loc[
    orders["order_status"] == "delivered",
    [
        "order_id",
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
].copy()

# Convert date columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in date_columns:
    delivery_data[column] = pd.to_datetime(
        delivery_data[column],
        errors="coerce"
    )

# Calculate actual delivery time in days
delivery_data["delivery_days"] = (
    delivery_data["order_delivered_customer_date"]
    - delivery_data["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Compare calendar dates to avoid treating the time of day
# as a delay when the estimated date is the same calendar day
actual_date = delivery_data[
    "order_delivered_customer_date"
].dt.normalize()

estimated_date = delivery_data[
    "order_estimated_delivery_date"
].dt.normalize()

delivery_data["delay_days"] = (
    actual_date - estimated_date
).dt.days

# Keep records with the dates needed for the analysis
valid_delivery = delivery_data.dropna(
    subset=[
        "delivery_days",
        "delay_days",
    ]
).copy()

# Classify delivery performance
late_orders = valid_delivery[
    valid_delivery["delay_days"] > 0
]

on_time_or_early_orders = valid_delivery[
    valid_delivery["delay_days"] <= 0
]

total_valid = len(valid_delivery)

late_rate = (
    len(late_orders) / total_valid * 100
    if total_valid > 0 else 0
)

print(f"Delivered orders: {len(delivery_data):,}")
print(f"Orders with complete delivery dates: {total_valid:,}")
print(
    "Orders excluded due to missing dates:",
    len(delivery_data) - total_valid
)
print(
    f"Average delivery time: "
    f"{valid_delivery['delivery_days'].mean():.2f} days"
)
print(f"Late orders: {len(late_orders):,}")
print(
    f"On-time or early orders: "
    f"{len(on_time_or_early_orders):,}"
)
print(f"Late delivery rate: {late_rate:.2f}%")
